# Example Application


# Building Docker Image
``` bash
% cd example-app
% ./build.sh
```


# Running Docker Image
```bash
% cd example-app
% ./run.sh
```

# Debugging Docker Image
``` bash
% ./run.sh bash
/app/python# ls
main.py
/app/python# python3 main.py
hello world
```

# Generating a Key
``` bash
% ./run.sh python3 tools/generate_key.py
wif = cVFvSok3fhw3eSZ2bjWJxotoUo5Yk5PoQBhdvn3sNEn3zgVeULjV
address = n1pkEsenMDNfpcXcFNqKymotfACTMxR1FX
```