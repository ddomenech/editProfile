from io import BytesIO

import pytest
from PIL import Image
from django.core.files.base import ContentFile
from django.urls import reverse_lazy


def create_image(storage, filename, size=(100, 100), image_mode='RGB',
                 image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


@pytest.fixture
def user_test(django_user_model):
    username = "pruebas_2"
    password = "dfdfdfdfdf"
    user = django_user_model.objects.create_user(username=username, password=password)
    return user


@pytest.mark.django_db
def test_unauthorized(client):
    url = reverse_lazy('user-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized(client, user_test):
    url = reverse_lazy('user-detail', kwargs={'pk': user_test.id})
    client.force_login(user_test)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_user_phone(client, user_test):
    client.force_login(user_test)
    url = reverse_lazy('user-detail', kwargs={'pk': user_test.id})
    response = client.patch(
        url, {'phone': '+34656324353'},
        content_type='application/json'
    )
    print(response.data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_user_avatar(client, user_test):
    url = reverse_lazy('user-detail', kwargs={'pk': user_test.id})
    client.force_login(user_test)
    av_f = create_image(None, './media/1483596196_757715_1483596586_noticia_normal.jpg')
    headers = {
        'HTTP_CONTENT_DISPOSITION': 'attachment; filename={}'.format('image.jpg'),
    }
    response = client.patch(url, data={'avatar': av_f}, format='multipart', **headers)
    assert response.status_code == 200



@pytest.mark.django_db
def test_user_change_password(client, django_user_model):
    user = django_user_model.objects.create(
        username='pruebas_3', password='aaaaaaaa'
    )
    user.set_password('aaaaaaaa')
    user.save()
    url = reverse_lazy('user-set-password', kwargs={'pk': user.id})
    client.force_login(user)
    response = client.put(
        url, {"old_password": "aaaaaaaa", "new_password": "bbbbbbbb"},
        content_type='application/json'
    )
    print(url)
    print(response.data)
    assert response.status_code == 200
