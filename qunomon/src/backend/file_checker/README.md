# FileChecker

# Input
inventory

# Output

```json
{
    "exists":True,
    "is_directory":False,
    "hash_sha256":"XXXXXXX"
}
```

# docker

## build

```
docker build .\file_checker -t file_checker:0.1
```

## run

```
docker run -v /C/testbed_mount_volume/ip/dummyInventory:/usr/local/qai/input -v /C/testbed_mount_volume:/usr/local/qai/output file_checker:0.1 test.csv 1
```