#!/usr/bin/env sh

# Copyright (C) 2024 Jack Green (jackgreen.co)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

set -e

DOMAINS="jackgreen.co blog.jackgreen.co"
CERT_PATH="/etc/ssl/public"
CA="${ACME_CA:-letsencrypt}"

issue_acme_cert() {
    echo "Issuing ACME certificate for ${domain}"
    domain=${1}

    mkdir -p "${CERT_PATH}/${domain}"
    /root/.acme.sh/acme.sh --issue -d "${domain}" --force --alpn --ocsp --server "${CA}" \
        --key-file "${CERT_PATH}/${domain}/privkey.pem" \
        --fullchain-file "${CERT_PATH}/${domain}/fullchain.pem" \
        --ca-file "${CERT_PATH}/${domain}/chain.pem"
}

renew_acme_cert() {
    domain=${1}

    exp_time="$(openssl x509 -noout -enddate -in "${CERT_PATH}/${domain}/fullchain.pem" | cut -d= -f2)"
    echo "Certificate for ${domain} expires at ${exp_time}"

    if openssl x509 -checkend 2592000 -noout -in "${CERT_PATH}/${domain}/fullchain.pem" >/dev/null 2>&1; then
        echo "Certificate for ${domain} is still valid for more than 30 days - skipping renewal"
        return
    fi

    echo "Renewing ACME certificate for ${domain}"
    /root/.acme.sh/acme.sh --issue -d "${domain}" --force --alpn --ocsp --server "${CA}" \
        --key-file "${CERT_PATH}/${domain}/privkey.pem" \
        --fullchain-file "${CERT_PATH}/${domain}/fullchain.pem" \
        --ca-file "${CERT_PATH}/${domain}/chain.pem"
}

issue_ss_cert() {
    echo "Issuing self-signed certificate for ${domain}"
    domain=${1}

    mkdir -p "${CERT_PATH}/${domain}"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/CN=${domain}" \
        -keyout "${CERT_PATH}/${domain}/privkey.pem" -out "${CERT_PATH}/${domain}/fullchain.pem" >/dev/null 2>&1
    cp "${CERT_PATH}/${domain}/fullchain.pem" "${CERT_PATH}/${domain}/chain.pem"
}

save_ocsp_response() {
    echo "Saving OCSP response for ${domain}"
    domain=${1}

    ocsp_url=$(openssl x509 -noout -ocsp_uri -in "${CERT_PATH}/${domain}/fullchain.pem")
    openssl ocsp -no_nonce -respout "${CERT_PATH}/${domain}/ocsp.der" -issuer "${CERT_PATH}/${domain}/chain.pem" \
        -cert "${CERT_PATH}/${domain}/fullchain.pem" -url "${ocsp_url}" >/dev/null 2>&1
}

if [ -z "${DOMAINS}" ]; then
    exit 1
fi

for domain in ${DOMAINS}; do
    if [ "${BUILD_ENV}" = "staging" ]; then
        issue_ss_cert "${domain}"
    elif [ -f "${CERT_PATH}/${domain}/privkey.pem" ]; then
        renew_acme_cert "${domain}"
        save_ocsp_response "${domain}"
    else
        issue_acme_cert "${domain}"
        save_ocsp_response "${domain}"
    fi
done

chown -R nginx:nginx "${CERT_PATH}"
