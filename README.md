# Randomized christmas!

Do you get too many christmas presents? What if you'd only get one and give one?

# Usage

Install all requirements:

```
poetry install
```

Check the constants at the top of `email.py`. Emails are sent using Amazon SES, so you must have everything setup correctly so that you can use the sender address defined as `JOULUPUKKI_EMAIL`.

To test that sending email works, run

```
poetry run python random_xmax/main.py --test-email YOUR_EMAIL_ADDRESS
```

Next create a data file of participants. This should be a json file with a single list where each element is an object like this:

```
{
    "name": "Mikko",
    "email": "mikko@example.com",
    "wishes": ["Eternal peace!", "Vihreitä kuulia!"]
}
```

Save the data as `data/tontut.json`. To test and see what kind of emails would be
send, do a dry run (this will _not_ send anything yet, just prints the emails to
stdout):

```
poetry run python random_xmax/main.py -d data/tontut.json
```

Note that you get a different permutation of givers and recipients on every run. The only limitation is that nobody will be assigned to themselves.

When all looks correct and you are ready to send the real emails, add flag `--merry-christmas`.

And Have a Merry Christmas! 🎅
