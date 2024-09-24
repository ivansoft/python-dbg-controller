# -*- coding: windows-1251 -*-

import mmap
import struct
import win32event  # pip install pywin32
import time
import sys


def QLuaControllerStart(Filter="QLua"):
    # ������� ������ ������� ���������� ������ ��� ��������� ���������� ���������
    buffer_ready = win32event.CreateEvent(None, 0, 0, "DBWIN_BUFFER_READY")
    # ������� ������ ������� ��������� ������ ����������� ���������
    data_ready = win32event.CreateEvent(None, 0, 0, "DBWIN_DATA_READY")
    # �������� ������ ��� ����� ������
    _buffer = mmap.mmap(0, 4096, "DBWIN_BUFFER", mmap.ACCESS_WRITE)

    while True:
        # ������������� ������� ���������� ������ ��� ��������� ���������� ���������,
        # �.�. ������������ "���������-�������"
        win32event.SetEvent(buffer_ready)
        # ���� ���� ������ ��������� ������ ����������� ��������� � ������������ ���
        if win32event.WaitForSingleObject(data_ready, 1) == win32event.WAIT_OBJECT_0:
            _buffer.seek(0)
            # �������� ������������� ��������, ������������ ���������� ���������
            process_id, = struct.unpack("L", _buffer.read(4))
            # ��������� ���������� ��������� �� ������ ������
            data = _buffer.read(4092)
            data_str = data.decode()
            #print(">>>", process_id, data_str)
            # ��������� ������ �� ������� ��������� ������, ���� �� ������������
            if "\0" in data_str:
                str1 = data_str[:data_str.index("\0")]
            # ����� ��� ������ � ������ �������� ���������� ����������
            else:
                str1 = data_str

            # ��������� ����������� ��������� Filter � ���������,
            # ���� ��� ������������, �������, ���
            # ���������� ��������� �������� �� ������ ������� Lua
            if str1.find(Filter) >= 0:
                ticks = time.localtime()
                # ������� ���������� ��������� � �������
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
