#!/usr/bin/env sh

# Copyright (C) 2024 Jack Green (jackgreen.co)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
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
opts_longopts="help,version,verbose,no-convert,no-resize,input:,output:"
opts_shortopts="hvVCRi:o:"
opts_usage="usage: ${opts_scriptname} [-h|--help] [-v|--version]"
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

        cp "${image}" "${output_path}/${image_name}-${width}.${image_extn}"

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
            -strip "${output_path}/${image_name}-${width}.${image_extn}"

        cwebp -m 6 -pass 10 -mt -quiet -q 80 "${output_path}/${image_name}-${width}.${image_extn}" \
            -o "${output_path}/${image_name}-${width}.webp"

        rm -f "${output_path}/${image_name}-${width}.${image_extn}"
    done

    if test "${verbose}"; then
        printf "converting ${image} to lqip...\n"
    fi 

    cp "${image}" "${output_path}/${image_name}-lqip.${image_extn}"

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
        -strip "${output_path}/${image_name}-lqip.${image_extn}"

    cwebp -m 6 -pass 10 -mt -quiet -q 80 "${output_path}/${image_name}-lqip.${image_extn}" \
        -o "${output_path}/${image_name}-lqip.webp"

    rm -f "${output_path}/${image_name}-lqip.${image_extn}"
}

convert_image "${input_file}" "${output_path}"
