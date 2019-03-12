# Methods Breakdown

## What is in the `request` object?

- `type`, string, will be a set number of values, like "HTTP URL",
  "Description", "IPFS Hash", etc
- `value`, string, stores the value associated with the request. For
  example, if `type` is `"description"`, then `value` could be
  `"Calculus textbook written by Joe Smith"`
- `user`, own object, contains thier username (and password?) that the
  request is associated with
- `date`, date object, the date and time in the object 
- `download status`, string, probably "true", "false" or "downloading"
- `file_location`, string (or file?), where the file has been
  downloaded to.
  
We could add things like file size, priotity, etc.

## `add_request(type, value, user)`

Written by Will, called by Nick. The will create a request object and
store the data in a database or CSV file. Could make more complicated
with fully defined data structure.

## `get_all_requests()`

Written by Will, called by Jake in `download_all_requests()`. This
will return a `list` of `request` objects.

## `download_all_requests()`

Could be called by Nick. This will call `get_all_requests()` and
actually execute the reqeuest. After it is done downloading, will call
`update_request(status, location)`. This will update the location of
the download and the status of the download.

## `update_request(status, location)`

Written by Will, called by Jake. This will update the location of the
download and the status of that request and write that to the database.
