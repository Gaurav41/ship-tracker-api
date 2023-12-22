from io import BytesIO
import json

def test_get_ships_api(client):
    res = client.get('/api/ships')
    assert res.status_code == 200
    assert b"IMO_number" in res.data
    assert b"name" in res.data


def test_get_positions_api(client):
    res = client.get('/api/positions/9632179')
    assert res.status_code == 200
    assert b"IMO_number" in res.data
    assert b"latitude" in res.data
    assert b"longitude" in res.data
    

def test_uplaod_position_csv(client):
    # file missing
    res = client.post('/api/load-position-data')
    assert res.status_code == 400
    assert b"File not received" in res.data

    csv_content = b'123,2019-01-15 09:44:27+00,51.87373352,4.56\n'

    # Mock file upload using test_client
    res = client.post('/api/load-position-data', data={'file': (BytesIO(csv_content), 'test.csv')}, content_type='multipart/form-data')
    assert res.status_code == 200
    assert b"Data inserted Succesfully" in res.data


def test_uplaod_ship_csv(client):
    pass