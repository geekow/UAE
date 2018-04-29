# UAE Challenge Repo

We focused our project on data collection because we think that there are already great researchers who are working on AI algorithms to exploit such a Dataset.
https://www.deepl.com/quality.html
(Deepl is a startup that is using DeepLearning to do translation and as you can see on the link, it's the best translation service that exists on the world (Over 50% better than Google/Facebook Translate or othere solutions)

This is the link of the smart contract we did on the Etherum Blockchain to give tokens to users:
https://ropsten.etherscan.io/token/0xae59cb888413900fb688be4948f04ae03a0c7d5d
(You have absolutely no obligation to use the blockchain our project could also work if we do it on a centralized based system.)

UAE.pdf is the pitch presentation

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

