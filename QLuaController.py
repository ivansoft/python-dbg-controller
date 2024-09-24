# -*- coding: windows-1251 -*-

import mmap
import struct
import win32event  # pip install pywin32
import time
import sys


def QLuaControllerStart(Filter="QLua"):
    # Создаем объект события готовности буфера для получения отладочных сообщений
    buffer_ready = win32event.CreateEvent(None, 0, 0, "DBWIN_BUFFER_READY")
    # Создаем объект события получения данных отладочного сообщения
    data_ready = win32event.CreateEvent(None, 0, 0, "DBWIN_DATA_READY")
    # Выделяем память под буфер обмена
    _buffer = mmap.mmap(0, 4096, "DBWIN_BUFFER", mmap.ACCESS_WRITE)

    while True:
        # Устанавливаем событие готовности буфера для получения отладочных сообщений,
        # т.е. регистрируем "программу-ловушку"
        win32event.SetEvent(buffer_ready)
        # Если есть сигнал получения данных отладочного сообщения – обрабатываем его
        if win32event.WaitForSingleObject(data_ready, 1) == win32event.WAIT_OBJECT_0:
            _buffer.seek(0)
            # Получаем идентификатор процесса, отправившего отладочное сообщение
            process_id, = struct.unpack("L", _buffer.read(4))
            # Считываем отладочное сообщение из буфера обмена
            data = _buffer.read(4092)
            data_str = data.decode()
            #print(">>>", process_id, data_str)
            # Считываем строку до символа окончания строки, если он присутствует
            if "\0" in data_str:
                str1 = data_str[:data_str.index("\0")]
            # иначе вся строка в буфере является отладочным сообщением
            else:
                str1 = data_str

            # Проверяем присутствие подстроки Filter в сообщении,
            # если она присутствует, считаем, что
            # отладочное сообщение получено от нашего скрипта Lua
            if str1.find(Filter) >= 0:
                ticks = time.localtime()
                # Выводим отладочное сообщение в консоль
                print("Pid %d [%02d:%02d:%02d]: %s" % (process_id,
                                                       ticks.tm_hour,
                                                       ticks.tm_min,
                                                       ticks.tm_sec,
                                                       str1))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        QLuaControllerStart()
    elif len(sys.argv) == 2:
        QLuaControllerStart(sys.argv[1])
