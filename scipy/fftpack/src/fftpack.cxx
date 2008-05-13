#include "fftpack.h"

/* The following macro convert private backend specific function to the public
 * functions exported by the module  */
#define GEN_ZFFT_API(name) \
extern "C" void zfft(complex_double *inout, int n, \
        int direction, int howmany, int normalize)\
{\
        zfft_##name(inout, n, direction, howmany, normalize);\
}

#define GEN_DRFFT_API(name) \
extern "C" void drfft(double *inout, int n, \
        int direction, int howmany, int normalize)\
{\
        drfft_##name(inout, n, direction, howmany, normalize);\
}

#define GEN_ZFFTND_API(name) \
extern "C" void zfftnd(complex_double * inout, int rank,\
		           int *dims, int direction, int howmany, int normalize)\
{\
        zfftnd_##name(inout, rank, dims, direction, howmany, normalize);\
}


/* ************** Definition of backend specific functions ********* */

/*
 * To add a backend :
 *  - create a file drfft_name.c, where you define a function drfft_name where
 *  name is the name of your backend. If you do not use the GEN_CACHE macro,
 *  you will need to define a function void destroy_drname_caches(void), 
 *  which can do nothing
 *  - in drfft.c, include the drfft_name.c file, and add the 3 following lines
 *  just after it:
 *  #ifndef WITH_DJBFFT
 *      GEN_PUBLIC_API(name)
 *  #endif
 */

#include "fftpack/drfft.cxx"
#include "fftpack/zfftnd.cxx"
#include "fftpack/zfft.cxx"

#if defined(WITH_FFTW) || defined(WITH_MKL)
static int equal_dims(int rank,int *dims1,int *dims2)
{
        int i;
        for (i = 0; i < rank; ++i) {
                if (dims1[i] != dims2[i]) {
                        return 0;
                }
        }
        return 1;
}
#endif

#ifdef WITH_FFTW3
    #include "fftw3/drfft.cxx"
    #include "fftw3/zfft.cxx"
    #include "fftw3/zfftnd.cxx"
    #ifndef WITH_DJBFFT
        GEN_ZFFT_API(fftw3)
        GEN_DRFFT_API(fftw3)
        GEN_ZFFTND_API(fftw3)
    #endif
#elif defined WITH_FFTW
    #include "fftw/drfft.cxx"
    #include "fftw/zfft.cxx"
    #include "fftw/zfftnd.cxx"
    #ifndef WITH_DJBFFT
        GEN_ZFFT_API(fftw)
        GEN_DRFFT_API(fftw)
        GEN_ZFFTND_API(fftw)
    #endif
#elif defined WITH_MKL
    #include "mkl/zfft.cxx"
    #include "mkl/zfftnd.cxx"
    #ifndef WITH_DJBFFT
        GEN_ZFFT_API(mkl)
        GEN_ZFFTND_API(mkl)
    #endif
    GEN_DRFFT_API(fftpack)
#endif

#if (!defined WITH_DJBFFT) && (!defined WITH_MKL) \
        && (!defined WITH_FFTW) && (!defined WITH_FFTW3)
GEN_ZFFT_API(fftpack)
GEN_DRFFT_API(fftpack)
GEN_ZFFTND_API(fftpack)
#endif 

/* 
 * djbfft must be used at the end, because it needs another backend (defined
 * above) for non 2^n * size 
 */
#ifdef WITH_DJBFFT
    #include "djbfft/drfft.cxx"
    #include "djbfft/zfft.cxx"
    GEN_DRFFT_API(djbfft)
    GEN_ZFFT_API(djbfft)
#endif
