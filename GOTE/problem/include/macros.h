#pragma once

#ifdef _WIN32
    #define EXPORT_DECL __declspec(dllexport)
#else
	#define EXPORT_DECL	__attribute__((visibility("default")))
#endif

#ifdef __cplusplus
#define C_EXPORT extern "C"
#else
#define C_EXPORT
#endif

#define EXPORT_API  C_EXPORT EXPORT_DECL
