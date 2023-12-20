from urllib.parse import quote
from fastapi import APIRouter
from starlette.responses import StreamingResponse
from service.data import FileModel
from type.functions import get_files

files_router = APIRouter()
file_model = FileModel()


# 根据下载链接下载文件
@files_router.get("/download/{id}")
async def file_download_files(id: int):
    file = file_model.get_file_info_by_id(id)
    pre_folder = file.hash_md5[:8] + '/' + file.hash_sha256[-8:]
    folder = pre_folder + '/' + file.name  # 先找到路径
    data = get_files(folder,1)
    encoded_filename = quote(file.name)
    headers = {
        "Content-Type": file.type,
        "Content-Disposition": f"inline; filename={encoded_filename}",
        "Cache-Control": "max-age=300"
    }
    return StreamingResponse(data, headers=headers)
