#!/usr/bin/env sh

set -e

DOMAINS="jackgreen.co blog.jackgreen.co"
CERT_PATH="/etc/ssl/public"
#CA="${ACME_CA:-letsencrypt}"
CA="letsencrypt_test"

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
    echo "Renewing ACME certificate for ${domain}"
    domain=${1}

    openssl x509 -checkend 86400 -noout -in "${CERT_PATH}/${domain}/fullchain.pem" || return

    /root/.acme.sh/acme.sh --renew -d "${domain}" --force --alpn --ocsp --server "${CA}" \
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

if [ ! -f "${CERT_PATH}/dhparam.pem" ]; then
    bits=4096

    if [ "${BUILD_ENV}" = "staging" ]; then
        bits=2048
    fi

    echo "Generating DH parameters (${bits} bits)"
    openssl dhparam -out "${CERT_PATH}/dhparam.pem" "${bits}" >/dev/null 2>&1
fi

chown -R 101:101 "${CERT_PATH}"
