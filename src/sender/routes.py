import codecs
import csv

from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from src.sender.schemas import SendMessageSchema
from src.sender.services.services import SenderService
from src.sender.dependencies import get_service


sender_router = APIRouter(
    prefix="/sender",
    tags=["sender", ]
)


@sender_router.post("/upload-accounts")
async def upload_accounts(
        sender_service: SenderService = Depends(get_service),
        file: UploadFile = File(...)
) -> JSONResponse:
    """
    Эндпоинт используемый для загрузки списка аккаунтов для рассылки
    file должен представлять собой файл с расширением csv.
    Первая строка файла должна иметь вид client_id, client_secret, code (названия столбцов).

    Для использования этого эндпоинта необходимо для каждого аккаунта, используемого для
    рассылки, создать приложение типа Standalone и в redirect_url при настройке прописать тот,
    что обозначен в .env. Client_id и client_secret будут доступны в настройках приложения
    как "ID приложения" и "Защищенный ключ" соответственно

    Для получения code для каждого аккаунта необходимо ввиду отсутствия
    фронтэнда произвести вручную следующее: сделать запрос на url в
    формате: https://oauth.vk.com/authorize?client_id=<YOUR_CLIENT_ID>&
    display=page&redirect_uri=<YOUR_REDIRECT_URI>&scope=messages&response_type=code&v=5.131,
    после чего пройти авторизацию и скопировать в csv файл код,
    который будет в параметре code url, на который вы будете перенаправлены
    """

    try:
        reader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))
        await sender_service.upload_accounts(
            accounts_data=[row for row in reader]
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this client_id already exists"
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect file format"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Accounts were successfully added"
        }
    )


@sender_router.delete("/delete-accounts")
async def delete_current_accounts(
        sender_service: SenderService = Depends(get_service)
) -> JSONResponse:
    """
    Эндпоинт, используемый для очистки списка аккаунтов, с которых идет рассылка, в случае,
    когда необходимо использовать новый список аккаунтов, а старый теряет надобность
    """

    await sender_service.delete_accounts()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "All current accounts were successfully deleted"
        }
    )


@sender_router.post("/upload-contacts")
async def upload_contacts(
        file: UploadFile = File(...),
        sender_service: SenderService = Depends(get_service)
) -> JSONResponse:
    """
    Эндпоинт, используемый для загрузки списка контактов для рассылки.
    file должен представлять собой файл с расширением csv, где в один столбец
    расположены vk_id пользователей, которым необходимо отправить сообщение
    """

    try:
        reader = csv.reader(codecs.iterdecode(file.file, "utf-8"))
        await sender_service.upload_contacts(
            contacts_data=[row for row in reader]
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with this vk_id already exists"
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect file format"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Contacts were successfully added"
        }
    )


@sender_router.delete("/delete-contacts")
async def delete_current_contacts(
        sender_service: SenderService = Depends(get_service)
) -> JSONResponse:
    """
    Эндпоинт, используемый для очистки списка контактов для рассылки, в случае,
    когда необходимо использовать новый список контактов, а старый теряет надобность
    """

    await sender_service.delete_contacts()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "All current contacts were successfully deleted"
        }
    )


@sender_router.post("/send-message")
async def send_message(
        body: SendMessageSchema,
        sender_service: SenderService = Depends(get_service),
) -> JSONResponse:
    """
    Эндпоинт, используемый для отправки сообщений контактам.
    minute, hour, day, month, year отвечают за момент времени, когда рассылка
    будет произведена. Момент времени, сформированный на основании этих параметров
    должен быть больше нынешнего. message - содержание сообщения для рассылки
    """

    await sender_service.send_message(**body.model_dump())

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "The mailing was successfully scheduled"
        }
    )
