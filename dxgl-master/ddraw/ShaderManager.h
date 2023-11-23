// DXGL
// Copyright (C) 2011-2016 William Feely

// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.

// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

#pragma once
#ifndef __SHADERMANAGER_H
#define __SHADERMANAGER_H

#ifdef __cplusplus
extern "C" {
#endif

extern const SHADER shader_template[];

#define PROG_TEXTURE 0
#define PROG_PAL256 1
#define PROG_CLIPSTENCIL 2

struct TEXTURESTAGE;
struct ShaderGen3D;

void ShaderManager_Init(glExtensions *glext, ShaderManager *shaderman);
void ShaderManager_Delete(ShaderManager *This);
void ShaderManager_SetShader(ShaderManager *This, __int64 id, __int64 *texstate, int type);

#ifdef __cplusplus
}
#endif

#endif //__SHADERMANAGER_H
