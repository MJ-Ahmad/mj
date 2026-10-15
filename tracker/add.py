#!/usr/bin/env python3

import os
import sys
import json
import shutil
import hashlib
import mimetypes

from datetime import (
    datetime,
    timezone,
    timedelta
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data.json"
)

REGISTRY_FILE = os.path.join(
    BASE_DIR,
    "registry.json"
)

ATTACHMENTS_DIR = os.path.join(
    BASE_DIR,
    "attachments"
)


def ensure_structure():

    os.makedirs(
        ATTACHMENTS_DIR,
        exist_ok=True
    )

    if not os.path.exists(DATA_FILE):

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {"entries": []},
                f,
                indent=4,
                ensure_ascii=False
            )

    if not os.path.exists(REGISTRY_FILE):

        with open(
            REGISTRY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {"last_registry": 0},
                f,
                indent=4
            )


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def sha256_file(path):

    digest = hashlib.sha256()

    with open(
        path,
        "rb"
    ) as f:

        for chunk in iter(
            lambda: f.read(4096),
            b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def get_times():

    utc_now = datetime.now(
        timezone.utc
    )

    dhaka_tz = timezone(
        timedelta(hours=6)
    )

    dhaka_now = utc_now.astimezone(
        dhaka_tz
    )

    return (
        dhaka_now.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3],

        utc_now.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]
    )


def build_attachment(
    reg_id,
    file_path
):

    filename = os.path.basename(
        file_path
    )

    extension = os.path.splitext(
        filename
    )[1]

    stored_name = (
        reg_id + extension
    )

    destination = os.path.join(
        ATTACHMENTS_DIR,
        stored_name
    )

    shutil.copy2(
        file_path,
        destination
    )

    filesize = os.path.getsize(
        destination
    )

    filehash = sha256_file(
        destination
    )

    mime_type = (
        mimetypes.guess_type(
            destination
        )[0]
        or
        "application/octet-stream"
    )

    return {

        "file":
        f"attachments/{stored_name}",

        "original":
        filename,

        "size":
        filesize,

        "type":
        mime_type,

        "sha256":
        filehash
    }


def main():

    if len(sys.argv) < 3:

        print()

        print(
            "Usage:"
        )

        print()

        print(
            'python3 add.py "Heading" "Description"'
        )

        print()

        print(
            'python3 add.py "Heading" "Description" "/path/file"'
        )

        sys.exit(1)

    ensure_structure()

    heading = sys.argv[1].strip()

    description = sys.argv[2].strip()

    data = load_json(
        DATA_FILE
    )

    registry = load_json(
        REGISTRY_FILE
    )

    reg_no = (
        registry["last_registry"] + 1
    )

    reg_id = (
        f"REG-{reg_no:06}"
    )

    dhaka_time, utc_time = (
        get_times()
    )

    entry = {

        "registry":
        reg_id,

        "dhaka_time":
        dhaka_time,

        "utc_time":
        utc_time,

        "heading":
        heading,

        "description":
        description
    }

    if len(sys.argv) >= 4:

        file_path = os.path.expanduser(
            sys.argv[3]
        )

        if not os.path.isfile(
            file_path
        ):

            print(
                f"File not found: {file_path}"
            )

            sys.exit(1)

        attachment = build_attachment(
            reg_id,
            file_path
        )

        entry[
            "attachment"
        ] = attachment

    data["entries"].insert(
        0,
        entry
    )

    registry[
        "last_registry"
    ] = reg_no

    save_json(
        DATA_FILE,
        data
    )

    save_json(
        REGISTRY_FILE,
        registry
    )

    print()

    print(
        "Entry Added Successfully"
    )

    print()

    print(
        f"Registry : {reg_id}"
    )

    print(
        f"Heading  : {heading}"
    )

    print(
        f"Dhaka    : {dhaka_time}"
    )

    print(
        f"UTC      : {utc_time}"
    )

    if "attachment" in entry:

        print(
            f"Attachment : {entry['attachment']['original']}"
        )

    print()


if __name__ == "__main__":
    main()
