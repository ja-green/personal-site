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

# file: optimize-image.sh
# date: 2024-01-12
# lang: sh
#
# compress and convert an image to various sizes in webp format and
# generate a lqip, placing the output files in a specified directory

# fn/report_fatal
# opts:
# - 1: message
#
# report a fatal error to stderr and exit
report_fatal() {
    printf "fatal: ${1}\n" >&2
    exit 1
}

opts_scriptname="optimise-image.sh"
opts_cache_dir="/tmp/${opts_scriptname}.cache"
opts_longopts="help,version,verbose,input:,output:,lqip,clean-cache,no-cache"
opts_shortopts="hvVi:o:"
opts_usage="usage: ${opts_scriptname} [-h|--help] [-v|--version] [-i|--input <file>] [-o|--output <path>]"
opts_version="0.0.1"

opts_parsed=$(getopt \
    --options="${opts_shortopts}" \
    --longoptions="${opts_longopts}" \
    --name "${opts_scriptname}" -- "${@}")

if test ${?} -ne 0; then
    printf "${opts_usage}\n"
    exit 1
fi

eval set -- "${opts_parsed}"

while true; do
    case "${1}" in
        -h|--help)
            printf "${opts_usage}\n"
            exit 0
            ;;
        -v|--version)
            printf "${opts_version}\n"
            exit 0
            ;;
        -V|--verbose)
            verbose=true
            shift
            ;;
        -i|--input)
            input_file="${2}"
            shift 2
            ;;
        -o|--output)
            output_path="${2}"
            shift 2
            ;;
        --lqip)
            lqip=true
            shift
            ;;
        --clean-cache)
            rm -rf "${opts_cache_dir}"
            exit 0
            ;;
        --no-cache)
            no_cache=true
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            report_fatal "internal error"
            exit 1
            ;;
    esac
done

if test -z "${input_file}"; then
    report_fatal "no input file specified"
fi

if test -z "${output_path}"; then
    report_fatal "no output directory specified"
fi

if test ! -f "${input_file}"; then
    report_fatal "input file does not exist"
fi

mkdir -p "${opts_cache_dir}"

# fn/convert_image
# opts:
# - 1: image
# - 2: output path
#
# convert an image to various sizes in webp format and generate a lqip
convert_image() {
    local image="${1}"
    local image_name="${1%.*}"; image_name="${image_name##*/}"
    local image_extn="${1##*.}"
    local output_path="${2}"

    local widths="1920 1600 1366 1024 768 640"

    for width in ${widths}; do
        if test "${verbose}"; then
            printf "converting ${image} to ${width}...\n"
        fi

        cp "${image}" "${output_path}/${image_name}-original.${image_extn}"

        magick "${output_path}/${image_name}-original.${image_extn}" "${output_path}/${image_name}-${width}.jpg"

        mogrify \
            -path "${output_path}" \
            -filter Triangle \
            -define filter:support=2 \
            -thumbnail "${width}" \
            -unsharp 0.25x0.25+8+0.065 \
            -dither None \
            -posterize 136 \
            -quality 82 \
            -define jpeg:fancy-upsampling=off \
            -define png:compression-filter=5 \
            -define png:compression-level=9 \
            -define png:compression-strategy=1 \
            -define png:exclude-chunk=all \
            -interlace none \
            -colorspace sRGB \
            -strip "${output_path}/${image_name}-${width}.jpg"

        cwebp -m 6 -pass 10 -mt -quiet -q 80 "${output_path}/${image_name}-${width}.jpg" \
            -o "${output_path}/${image_name}-${width}.webp"

        rm -f "${output_path}/${image_name}-original.${image_extn}"

        update_cache "${image_hash}" "${output_path}/${image_name}-${width}.jpg"
        update_cache "${image_hash}" "${output_path}/${image_name}-${width}.webp"
    done

    if test "${lqip}"; then
        if test "${verbose}"; then
            printf "converting ${image} to lqip...\n"
        fi

        cp "${image}" "${output_path}/${image_name}-original.${image_extn}"

        magick "${output_path}/${image_name}-original.${image_extn}" "${output_path}/${image_name}-lqip.jpg" 

        mogrify \
            -path "${output_path}" \
            -filter Triangle \
            -define filter:support=2 \
            -thumbnail "20" \
            -unsharp 0.25x0.25+8+0.065 \
            -dither None \
            -posterize 136 \
            -quality 82 \
            -define jpeg:fancy-upsampling=off \
            -define png:compression-filter=5 \
            -define png:compression-level=9 \
            -define png:compression-strategy=1 \
            -define png:exclude-chunk=all \
            -interlace none \
            -colorspace sRGB \
            -strip "${output_path}/${image_name}-lqip.jpg"

        cwebp -m 6 -pass 10 -mt -quiet -q 80 "${output_path}/${image_name}-lqip.jpg" \
            -o "${output_path}/${image_name}-lqip.webp"

        rm -f "${output_path}/${image_name}-original.${image_extn}"

        update_cache "${image_hash}" "${output_path}/${image_name}-lqip.jpg"
        update_cache "${image_hash}" "${output_path}/${image_name}-lqip.webp"
    fi
}

# fn/generate_hash
# opts:
# - 1: image
#
# generate a sha1 hash for an image
generate_hash() {
    (printf "${1}:${lqip}" && cat "${1}") | sha1sum | awk '{print $1}'
}

# fn/create_cache
# opts:
# - 1: image hash
#
# create the image cache directory
create_cache() {
    local image_hash="${1}"

    mkdir -p "${opts_cache_dir}/${image_hash}"
}

# fn/check_cache
# opts:
# - 1: image name
# - 2: image hash
#
# check if an image hash is in the cache
check_cache() {
    local image_name="${1}"
    local image_hash="${2}"
    local cache_dir="${opts_cache_dir}/${image_hash}"

    if [[ -d "${cache_dir}" ]]; then
        if test "${verbose}"; then
            printf "${image_name} is up to date in cache. restoring...\n"
        fi

        return 0
    fi

    return 1
}

# fn/update_cache
# opts:
# - 1: image hash
# - 2: image path
#
# update the image cache with the the processed image
update_cache() {
    local image_hash="${1}"
    local image_path="${2}"
    local cache_dir="${opts_cache_dir}/${image_hash}"

    cp "${image_path}" "${cache_dir}"
}

# fn/restore_from_cache
# opts:
# - 1: image hash
# - 2: output path
#
# restore an image from the cache
restore_from_cache() {
    local image_hash="${1}"
    local output_path="${2}"
    local cache_dir="${opts_cache_dir}/${image_hash}"

    cp "${cache_dir}"/* "${output_path}"
}

# fn/main
#
# main entry point
main() {
    local image_hash=$(generate_hash "${input_file}")

    if ! test "${no_cache}" && check_cache "${input_file}" "${image_hash}"; then
        restore_from_cache "${image_hash}" "${output_path}"
        return
    fi

    create_cache "${image_hash}"

    convert_image "${input_file}" "${output_path}"
}

main
