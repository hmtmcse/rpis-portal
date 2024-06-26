from pf_flask_web.system12.pweb_registry import PWebRegistry
from pf_py_file.pfpf_file_util import PFPFFileUtil


class RPIAssetsConfig:
    profile = PFPFFileUtil.join_path(PWebRegistry.config.UPLOADED_STATIC_RESOURCES, "profile")
    cover = PFPFFileUtil.join_path(PWebRegistry.config.UPLOADED_STATIC_RESOURCES, "cover")
    pdf = PFPFFileUtil.join_path(PWebRegistry.config.UPLOADED_STATIC_RESOURCES, "pdf")
    qrcode = PFPFFileUtil.join_path(PWebRegistry.config.UPLOADED_STATIC_RESOURCES, "qrcode")
    register = PFPFFileUtil.join_path(PWebRegistry.config.UPLOADED_STATIC_RESOURCES, "register")
    prove = PFPFFileUtil.join_path(PWebRegistry.config.UPLOADED_STATIC_RESOURCES, "prove")
