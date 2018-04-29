# UAE Challenge Repo

### Requirements:

- Docker
- Docker Compose

### How to launch the project:

```bash
docker-compose up
```

# Api routes

- On errors the api will respond a json like this:
```json
{"status": "error", "message": $ERROR_MSG}
```

Add a user translation
------
```bash
curl -X POST -i http://$HOSTNAME/add_user_trad --data '{
  "arabic": $ARABIC_WORD,
  "english": $ENGLISH_WORD"
}
'
```

Ask a word translation
------

```bash
curl -X GET -i http://$HOSTNAME/ask_traduction/arabic/testenglish 
```
- Word translation answer:
```json
{"status": "success", "result": $TRANSLATED_WORD}
```

Get a word that require translation
------

```bash
curl -X GET -i http://$HOSTNAME/get_word_to_traduce/$LANGUAGETOTRADUCE
```
- JSON Answer:
```json
{"status": "success", "result": $WORD_TO_TRADUCE}
```

### Useful information's:

- UAE Api xml content in the folder UAE

- Smart contract model defined in file Contract.txt

