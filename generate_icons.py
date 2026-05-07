#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成简单的占位图标
用于项目模板的默认图标
"""

import struct
import zlib
from pathlib import Path


def create_simple_ico(output_path: str, size: int = 256) -> bool:
    """
    创建一个简单的 ICO 文件
    
    Args:
        output_path: 输出路径
        size: 图标尺寸
        
    Returns:
        bool: 是否成功
    """
    try:
        # 创建一个简单的 PNG 数据（蓝色方块）
        def create_png(width: int, height: int, color: tuple) -> bytes:
            """创建简单的 PNG 图像"""
            # PNG 文件头
            signature = b'\x89PNG\r\n\x1a\n'
            
            # IHDR chunk
            ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
            ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
            ihdr = struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
            
            # IDAT chunk (简单的蓝色填充)
            raw_data = b''
            for y in range(height):
                raw_data += b'\x00'  # 过滤类型
                for x in range(width):
                    raw_data += bytes(color)  # RGB
            
            compressed = zlib.compress(raw_data, 9)
            idat_crc = zlib.crc32(b'IDAT' + compressed)
            idat = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)
            
            # IEND chunk
            iend_crc = zlib.crc32(b'IEND')
            iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
            
            return signature + ihdr + idat + iend
        
        # 创建蓝色图标 (匹配主题色)
        blue_color = (79, 140, 255)  # #4F8CFF
        png_data = create_png(size, size, blue_color)
        
        # ICO 文件结构
        # ICONDIR
        icondir = struct.pack('<HHH', 0, 1, 1)
        
        # ICONDIRENTRY
        width_byte = size if size < 256 else 0
        height_byte = size if size < 256 else 0
        icondirentry = struct.pack('<BBBBHHII', 
            width_byte,  # 宽度
            height_byte,  # 高度
            0,  # 调色板颜色数
            0,  # 颜色平面
            1,  # 每像素位数
            32,  # 每像素位数
            len(png_data),  # 图像数据大小
            22  # 图像数据偏移量 (6 + 16)
        )
        
        # 写入文件
        with open(output_path, 'wb') as f:
            f.write(icondir)
            f.write(icondirentry)
            f.write(png_data)
        
        return True
    except Exception as e:
        print(f"Error creating ICO: {e}")
        return False


def create_simple_png(output_path: str, width: int = 256, height: int = 256) -> bool:
    """
    创建一个简单的 PNG 文件
    
    Args:
        output_path: 输出路径
        width: 宽度
        height: 高度
        
    Returns:
        bool: 是否成功
    """
    try:
        # PNG 文件头
        signature = b'\x89PNG\r\n\x1a\n'
        
        # IHDR chunk
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
        ihdr = struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
        
        # IDAT chunk (蓝色填充)
        blue_color = (79, 140, 255)  # #4F8CFF
        raw_data = b''
        for y in range(height):
            raw_data += b'\x00'  # 过滤类型
            for x in range(width):
                raw_data += bytes(blue_color)  # RGB
        
        compressed = zlib.compress(raw_data, 9)
        idat_crc = zlib.crc32(b'IDAT' + compressed)
        idat = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)
        
        # IEND chunk
        iend_crc = zlib.crc32(b'IEND')
        iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
        
        # 写入文件
        with open(output_path, 'wb') as f:
            f.write(signature + ihdr + idat + iend)
        
        return True
    except Exception as e:
        print(f"Error creating PNG: {e}")
        return False


def main():
    """生成图标文件"""
    # 项目根目录
    root = Path(__file__).parent
    
    # 生成 app.ico
    ico_path = root / 'app.ico'
    if create_simple_ico(str(ico_path)):
        print(f"Created: {ico_path}")
    else:
        print(f"Failed to create: {ico_path}")
    
    # 生成 logo.png
    png_path = root / 'logo.png'
    if create_simple_png(str(png_path)):
        print(f"Created: {png_path}")
    else:
        print(f"Failed to create: {png_path}")
    
    print("\nDone! You can replace these placeholder icons with your own designs.")


if __name__ == '__main__':
    main()
