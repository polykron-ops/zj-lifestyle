"""Read-only, counted, stop-on-403 client for the zj1-images Space (cl, Scope A only).
Uses only SPACE_KEY_ID / SPACE_KEY_SECRET / SPACE_ENDPOINT / SPACE_BUCKET. Never prints a secret.
Operations: list_objects_v2 and ranged get_object. Nothing else exists in this module."""
import os, sys, json, boto3
from botocore.config import Config
from botocore.exceptions import ClientError

COUNTS = {"list": 0, "get": 0, "bytes": 0}
class Stop(Exception): pass

def client():
    ep = os.environ["SPACE_ENDPOINT"]
    if "://" not in ep: ep = "https://" + ep
    return boto3.client("s3", endpoint_url=ep,
        aws_access_key_id=os.environ["SPACE_KEY_ID"],
        aws_secret_access_key=os.environ["SPACE_KEY_SECRET"],
        config=Config(retries={"max_attempts": 2}, signature_version="s3v4"))

def _guard(e):
    code = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if code == 403: raise Stop("403 -- stopping per grant: %s" % e.response.get("Error", {}).get("Code"))
    raise e

def ls(c, prefix="", delimiter=None, max_keys=20):
    COUNTS["list"] += 1
    kw = dict(Bucket=os.environ["SPACE_BUCKET"], Prefix=prefix, MaxKeys=max_keys)
    if delimiter: kw["Delimiter"] = delimiter
    try: return c.list_objects_v2(**kw)
    except ClientError as e: _guard(e)

def rng(c, key, n=65536):
    COUNTS["get"] += 1
    try:
        r = c.get_object(Bucket=os.environ["SPACE_BUCKET"], Key=key, Range="bytes=0-%d" % (n - 1))
        b = r["Body"].read(); COUNTS["bytes"] += len(b); return b
    except ClientError as e: _guard(e)

if __name__ == "__main__":
    c = client(); r = ls(c, "", "/", 1000)
    print("prefixes:", [p["Prefix"] for p in r.get("CommonPrefixes", [])])
    print("root keys:", [(k["Key"], k["Size"]) for k in r.get("Contents", [])][:10], "truncated:", r.get("IsTruncated"))
    print(json.dumps(COUNTS))
