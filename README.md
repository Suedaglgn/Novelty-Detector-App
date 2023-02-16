# Novelty Detection App on Time Series Data

### Data
ambient_temperature_system_failure.csv from [The Numenta Anomaly Benchmark (NAB)](https://github.com/numenta/NAB)

### Techniques

- EllipticEnvelope
- CatBoost

### Usage

1- Run ipynb file to create model

2- Build docker file in project directory

```commandline
docker build -t novelty_detector .
```
3- Run docker image

```commandline
docker run -p 5000:5000 novelty_detector
```

4- Use postman or curl to predict

Curl:

```curl
curl --location --request POST 'http://127.0.0.0:5000/predict' \
--header 'Content-Type: application/json' \
--data-raw '{
    "value": 13
}'
```

Json:

```json
{
    "value": 13
}
```


### API docs


| Endpoints | Method | Params |         Definition         | Sample Value | Sample Response                                      |
|:---------:|:------:|:------:|:--------------------------:|:------------:|------------------------------------------------------|
| /predict  |  POST  | value  | Value that want to predict |      13      | {'prediction': [1]}                                  |
|  /report  |  GET   |   -    |             -              |      -       | Number of normal values and Number of anormal values |


## Result

                  precision    recall  f1-score   support
    
               0       1.00      1.00      1.00      1797
               1       1.00      0.90      0.95        20
    
        accuracy                           1.00      1817
       macro avg       1.00      0.95      0.97      1817
    weighted avg       1.00      1.00      1.00      1817