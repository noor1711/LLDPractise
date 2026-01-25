import requests
categories = ["Programming", "Misc", "Pun", "Spooky", "Christmas"];
params = ["blacklistFlags=nsfw,religious,racist", "idRange=0-100"];

response = requests.get("https://v2.jokeapi.dev/joke/" + ",".join(categories) + "?" + "&".join(params))

print(response)
res = response.json()

if "joke" in res:
    print(res["joke"])
else:
    setup, delivery = res["setup"], res["delivery"]
    print(setup, delivery)