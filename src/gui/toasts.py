from pyqttoast import Toast, ToastPreset, ToastPosition


def success_toast(title: str, text: str):
    toast = Toast()
    toast.setDuration(6000)
    toast.setTitle(title)
    toast.setText(text)
    toast.applyPreset(ToastPreset.SUCCESS)
    toast.setPosition(ToastPosition.TOP_MIDDLE)
    toast.show()


def error_toast(title: str, text: str):
    toast = Toast()
    toast.setDuration(8000)
    toast.setTitle(title)
    toast.setText(text)
    toast.applyPreset(ToastPreset.ERROR)
    toast.setPosition(ToastPosition.TOP_MIDDLE)
    toast.show()
