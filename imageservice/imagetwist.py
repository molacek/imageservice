import hashlib


def validate(thumb_url, sess):
    r = sess.get(thumb_url)
    if r.status_code == 404:
        return "not_found"

    if "Content-Type" not in r.headers:
        return "not_found"

    if "Content-Length" not in r.headers:
        return "not_found"

    if r.headers["Content-Length"] == "8183":
        image_md5 = hashlib.md5(r.content).hexdigest()
        if image_md5 == "0bc8d04776c8eac2a12568d109162249":
            return "not_found"

    return "ok"
