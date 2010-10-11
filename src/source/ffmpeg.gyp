# Copyright (c) 2010 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# There's a couple key GYP variables that control how FFmpeg is built:
#   ffmpeg_branding
#     Controls whether we build the Chromium or Google Chrome version of
#     FFmpeg.  The Google Chrome version contains additional codecs.
#     Typical values are Chromium, Chrome, ChromiumOS, and ChromeOS.
#   use_system_ffmpeg
#     When set to non-zero will build Chromium against the system FFmpeg
#     headers via pkg-config.  When Chromium is launched it will assume that
#     FFmpeg is present in the system library path.  Default value is 0.
#   build_ffmpegsumo
#     When set to zero will build Chromium against the patched ffmpegsumo
#     headers, but not build ffmpegsumo itself.  Users are expected to build
#     and provide their own version of ffmpegsumo.  Default value is 1.
#  use_system_vpx
#     When set to non-zero, will build Chromium against the system libvpx.
#     libvpx doesn't currently supply a pkg-config file, so we assume that
#     -lvpx is sufficient.

{
  'target_defaults': {
    'conditions': [
      ['OS!="linux" and OS!="freebsd" and OS!="openbsd" and OS!="solaris"', {
        'sources/': [['exclude', '/linux/']]
      }],
      ['OS!="mac"', {'sources/': [['exclude', '/mac/']]}],
      ['OS!="win"', {'sources/': [['exclude', '/win/']]}],
    ],
    'variables': {
      # Since we are not often debugging FFmpeg, and performance is
      # unacceptable without optimization, freeze the optimizations to -O2.
      # If someone really wants -O1 , they can change these in their checkout.
      # If you want -O0, see the Gotchas in README.Chromium for why that
      # won't work.
      'debug_optimize': '2',
      'mac_debug_optimization': '2',
    },
  },
  'variables': {
    # Allow overridding the selection of which FFmpeg binaries to copy via an
    # environment variable.  Affects the ffmpeg_binaries target.

    'conditions': [
      ['chromeos==1', {
        'ffmpeg_branding%': '<(branding)OS',
      }, {  # otherwise, assume Chrome/Chromium.
        'ffmpeg_branding%': '<(branding)',
      }],
      ['armv7==1 and arm_neon==1', {
        # Need a separate config for arm+neon vs arm
        'ffmpeg_config%': 'arm-neon',
      }, {
        'ffmpeg_config%': '<(target_arch)',
      }],
      ['target_arch=="x64" or target_arch=="ia32"', {
        'ffmpeg_asm_lib': 1,
      }],
      ['target_arch=="arm"', {
        'ffmpeg_asm_lib': 0,
      }],

      # libvpx location.
      # TODO(scherkus): libvpx_hack_dir is a hack to make -L work on linux.
      ['OS=="mac" or OS=="win"', {
        'libvpx_incl_dir': '../libvpx/include',
        'libvpx_hack_dir': '../libvpx',
      }],
      ['OS!="mac" and OS!="win" and inside_chromium_build==1', {
        'libvpx_incl_dir': '../libvpx/include',
        'libvpx_hack_dir': 'third_party/libvpx',
      }],
      ['OS!="mac" and OS!="win" and inside_chromium_build==0', {
        'libvpx_incl_dir': '../libvpx/include',
        'libvpx_hack_dir': 'WebKit/chromium/third_party/libvpx',
      }],
    ],
    'ffmpeg_variant%': '<(target_arch)',

    'use_system_ffmpeg%': 0,
    'use_system_yasm%': 0,
    'build_ffmpegsumo%': 1,
    'use_system_vpx%': 0,

    # Locations for generated artifacts.
    'shared_generated_dir': '<(SHARED_INTERMEDIATE_DIR)/third_party/ffmpeg',
    'asm_library': 'ffmpegasm',
  },
  'conditions': [
    ['OS!="win" and use_system_ffmpeg==0 and build_ffmpegsumo!=0', {
      'targets': [
        {
          'target_name': 'ffmpegsumo',
          'type': 'shared_library',
          'sources': [
            'patched-ffmpeg-mt/libavcodec/allcodecs.c',
            'patched-ffmpeg-mt/libavcodec/audioconvert.c',
            'patched-ffmpeg-mt/libavcodec/avpacket.c',
            'patched-ffmpeg-mt/libavcodec/bitstream.c',
            'patched-ffmpeg-mt/libavcodec/bitstream_filter.c',
            'patched-ffmpeg-mt/libavcodec/dsputil.c',
            'patched-ffmpeg-mt/libavcodec/faanidct.c',
            'patched-ffmpeg-mt/libavcodec/fft.c',
            'patched-ffmpeg-mt/libavcodec/golomb.c',
            'patched-ffmpeg-mt/libavcodec/imgconvert.c',
            'patched-ffmpeg-mt/libavcodec/jrevdct.c',
            'patched-ffmpeg-mt/libavcodec/libvpxdec.c',
            'patched-ffmpeg-mt/libavcodec/mdct.c',
            'patched-ffmpeg-mt/libavcodec/mpeg12data.c',
            'patched-ffmpeg-mt/libavcodec/mpeg4audio.c',
            'patched-ffmpeg-mt/libavcodec/opt.c',
            'patched-ffmpeg-mt/libavcodec/options.c',
            'patched-ffmpeg-mt/libavcodec/parser.c',
            'patched-ffmpeg-mt/libavcodec/pthread.c',
            'patched-ffmpeg-mt/libavcodec/raw.c',
            'patched-ffmpeg-mt/libavcodec/simple_idct.c',
            'patched-ffmpeg-mt/libavcodec/utils.c',
            'patched-ffmpeg-mt/libavcodec/vorbis.c',
            'patched-ffmpeg-mt/libavcodec/vorbis_data.c',
            'patched-ffmpeg-mt/libavcodec/vorbis_dec.c',
            'patched-ffmpeg-mt/libavcodec/vp3.c',
            'patched-ffmpeg-mt/libavcodec/vp3dsp.c',
            'patched-ffmpeg-mt/libavcodec/xiph.c',
            'patched-ffmpeg-mt/libavcore/imgutils.c',  # aug 11
            'patched-ffmpeg-mt/libavcore/parseutils.c',  # aug 11
            'patched-ffmpeg-mt/libavformat/allformats.c',
            'patched-ffmpeg-mt/libavformat/avi.c',
            'patched-ffmpeg-mt/libavformat/avio.c',
            'patched-ffmpeg-mt/libavformat/aviobuf.c',
            'patched-ffmpeg-mt/libavformat/cutils.c',
            'patched-ffmpeg-mt/libavformat/id3v1.c',
            'patched-ffmpeg-mt/libavformat/isom.c',
            'patched-ffmpeg-mt/libavformat/matroska.c',
            'patched-ffmpeg-mt/libavformat/matroskadec.c',
            'patched-ffmpeg-mt/libavformat/metadata.c',
            'patched-ffmpeg-mt/libavformat/metadata_compat.c',
            'patched-ffmpeg-mt/libavformat/oggdec.c',
            'patched-ffmpeg-mt/libavformat/oggparseogm.c',
            'patched-ffmpeg-mt/libavformat/oggparseskeleton.c',  # new
            'patched-ffmpeg-mt/libavformat/oggparsetheora.c',
            'patched-ffmpeg-mt/libavformat/oggparsevorbis.c',
            'patched-ffmpeg-mt/libavformat/options.c',
            'patched-ffmpeg-mt/libavformat/riff.c',
            'patched-ffmpeg-mt/libavformat/rm.c',
            'patched-ffmpeg-mt/libavformat/rmdec.c',
            'patched-ffmpeg-mt/libavformat/utils.c',
            'patched-ffmpeg-mt/libavformat/vorbiscomment.c',
            'patched-ffmpeg-mt/libavutil/avstring.c',
            'patched-ffmpeg-mt/libavutil/base64.c',
            'patched-ffmpeg-mt/libavutil/crc.c',
            'patched-ffmpeg-mt/libavutil/eval.c',
            'patched-ffmpeg-mt/libavutil/intfloat_readwrite.c',
            'patched-ffmpeg-mt/libavutil/inverse.c',  # aug 11
            'patched-ffmpeg-mt/libavutil/log.c',
            'patched-ffmpeg-mt/libavutil/lzo.c',
            'patched-ffmpeg-mt/libavutil/mathematics.c',
            'patched-ffmpeg-mt/libavutil/mem.c',
            'patched-ffmpeg-mt/libavutil/pixdesc.c',
            'patched-ffmpeg-mt/libavutil/rational.c',
            # Config file for the OS and architecture.
            'config/<(ffmpeg_branding)/<(OS)/<(ffmpeg_config)/config.h',
            'config/libavutil/avconfig.h',
          ],
          'include_dirs': [
            'config/<(ffmpeg_branding)/<(OS)/<(ffmpeg_config)',
            'patched-ffmpeg-mt',
            'config',
          ],
          'defines': [
            'HAVE_AV_CONFIG_H',
            '_POSIX_C_SOURCE=200112',
          ],
          'cflags': [
            '-fomit-frame-pointer',
          ],
          'conditions': [
            ['ffmpeg_branding=="Chrome" or ffmpeg_branding=="ChromeOS"', {
              'sources': [
                'patched-ffmpeg-mt/libavcodec/aacadtsdec.c',  #new
		'patched-ffmpeg-mt/libavcodec/aacdec.c',
                'patched-ffmpeg-mt/libavcodec/aacps.c',  # new
                'patched-ffmpeg-mt/libavcodec/aacsbr.c',
                'patched-ffmpeg-mt/libavcodec/aactab.c',
                'patched-ffmpeg-mt/libavcodec/cabac.c',
                'patched-ffmpeg-mt/libavcodec/error_resilience.c',
                'patched-ffmpeg-mt/libavcodec/h264.c',
                'patched-ffmpeg-mt/libavcodec/h264_cabac.c',
                'patched-ffmpeg-mt/libavcodec/h264_cavlc.c',
                'patched-ffmpeg-mt/libavcodec/h264_direct.c',
                'patched-ffmpeg-mt/libavcodec/h264_loopfilter.c',
                'patched-ffmpeg-mt/libavcodec/h264_mp4toannexb_bsf.c',
                'patched-ffmpeg-mt/libavcodec/h264_ps.c',
                'patched-ffmpeg-mt/libavcodec/h264_refs.c',
                'patched-ffmpeg-mt/libavcodec/h264_sei.c',
                'patched-ffmpeg-mt/libavcodec/h264dsp.c',
                'patched-ffmpeg-mt/libavcodec/h264idct.c',
                'patched-ffmpeg-mt/libavcodec/h264pred.c',
                'patched-ffmpeg-mt/libavcodec/mpegaudio.c',
                'patched-ffmpeg-mt/libavcodec/mpegaudio_parser.c',
                'patched-ffmpeg-mt/libavcodec/mpegaudiodata.c',
                'patched-ffmpeg-mt/libavcodec/mpegaudiodec.c',
                'patched-ffmpeg-mt/libavcodec/mpegaudiodecheader.c',
                'patched-ffmpeg-mt/libavcodec/mpegvideo.c',
                'patched-ffmpeg-mt/libavcodec/rdft.c',
                'patched-ffmpeg-mt/libavformat/gxf.c',
                'patched-ffmpeg-mt/libavformat/id3v2.c',
                'patched-ffmpeg-mt/libavformat/mov.c',
                'patched-ffmpeg-mt/libavformat/mp3.c',
              ],
            }],  # ffmpeg_branding
            ['ffmpeg_branding=="ChromiumOS" or ffmpeg_branding=="ChromeOS"', {
              'sources': [
                'patched-ffmpeg-mt/libavcodec/pcm.c',
                'patched-ffmpeg-mt/libavformat/raw.c',
                'patched-ffmpeg-mt/libavformat/wav.c',
              ],
            }],  # ffmpeg_branding
            ['ffmpeg_branding=="ChromeOS"', {
              'sources': [
                'patched-ffmpeg-mt/libavcodec/aandcttab.c',
                'patched-ffmpeg-mt/libavcodec/error_resilience.c',
                'patched-ffmpeg-mt/libavcodec/faandct.c',
                'patched-ffmpeg-mt/libavcodec/h263.c',
                'patched-ffmpeg-mt/libavcodec/h263_parser.c',
                'patched-ffmpeg-mt/libavcodec/h263dec.c',
                'patched-ffmpeg-mt/libavcodec/h264_mp4toannexb_bsf.c',
                'patched-ffmpeg-mt/libavcodec/intrax8.c',
                'patched-ffmpeg-mt/libavcodec/intrax8dsp.c',
                'patched-ffmpeg-mt/libavcodec/ituh263dec.c',
                'patched-ffmpeg-mt/libavcodec/ituh263enc.c',
                'patched-ffmpeg-mt/libavcodec/jfdctint.c',
                'patched-ffmpeg-mt/libavcodec/jfdctfst.c',
                'patched-ffmpeg-mt/libavcodec/motion_est.c',
                'patched-ffmpeg-mt/libavcodec/mpeg4data.h',
                'patched-ffmpeg-mt/libavcodec/mpeg4video.c',
                'patched-ffmpeg-mt/libavcodec/mpeg4video.h',
                'patched-ffmpeg-mt/libavcodec/mpeg4video_parser.c',
                'patched-ffmpeg-mt/libavcodec/mpeg4video_es_bsf.c',
                'patched-ffmpeg-mt/libavcodec/mpeg4videoenc.c',
                'patched-ffmpeg-mt/libavcodec/mpeg4videodec.c',
                'patched-ffmpeg-mt/libavcodec/mpegvideo.c',
                'patched-ffmpeg-mt/libavcodec/mpegvideo_enc.c',
                'patched-ffmpeg-mt/libavcodec/msmpeg4.c',
                'patched-ffmpeg-mt/libavcodec/msmpeg4data.c',
                'patched-ffmpeg-mt/libavcodec/ratecontrol.c',
                'patched-ffmpeg-mt/libavcodec/vc1.c',
                'patched-ffmpeg-mt/libavcodec/vc1data.c',
                'patched-ffmpeg-mt/libavcodec/vc1dec.c',
                'patched-ffmpeg-mt/libavcodec/vc1dsp.c',
                'patched-ffmpeg-mt/libavcodec/wma.c',
                'patched-ffmpeg-mt/libavcodec/wmadec.c',
                'patched-ffmpeg-mt/libavcodec/wmaprodec.c',
                'patched-ffmpeg-mt/libavcodec/wmv2.c',
                'patched-ffmpeg-mt/libavcodec/wmv2dec.c',
                'patched-ffmpeg-mt/libavcodec/vc1_asftoannexg_bsf.c',
                'patched-ffmpeg-mt/libavcodec/vc1_asftorcv_bsf.c',
                'patched-ffmpeg-mt/libavformat/asf.c',
                'patched-ffmpeg-mt/libavformat/asfcrypt.c',
                'patched-ffmpeg-mt/libavformat/asfdec.c',
                'patched-ffmpeg-mt/libavformat/avidec.c',
                'patched-ffmpeg-mt/libavformat/avlanguage.c',
                'patched-ffmpeg-mt/libavutil/des.c',
                'patched-ffmpeg-mt/libavutil/rc4.c',
              ],
            }],  # ffmpeg_branding
            ['target_arch=="ia32" or target_arch=="x64"', {
              'dependencies': [
                'make_ffmpeg_asm_lib',
              ],
              'sources': [
                'patched-ffmpeg-mt/libavcodec/x86/cpuid.c',
                'patched-ffmpeg-mt/libavcodec/x86/dsputil_mmx.c',
                'patched-ffmpeg-mt/libavcodec/x86/fdct_mmx.c',
                'patched-ffmpeg-mt/libavcodec/x86/fft.c',
                'patched-ffmpeg-mt/libavcodec/x86/fft_3dn.c',
                'patched-ffmpeg-mt/libavcodec/x86/fft_3dn2.c',
                'patched-ffmpeg-mt/libavcodec/x86/fft_sse.c',
                'patched-ffmpeg-mt/libavcodec/x86/idct_mmx_xvid.c',
                'patched-ffmpeg-mt/libavcodec/x86/idct_sse2_xvid.c',
                'patched-ffmpeg-mt/libavcodec/x86/simple_idct_mmx.c',
                'patched-ffmpeg-mt/libavcodec/x86/vp3dsp_mmx.c',
                'patched-ffmpeg-mt/libavcodec/x86/vp3dsp_sse2.c',
              ],
            }],
            ['(target_arch=="ia32" or target_arch=="x64") and (ffmpeg_branding=="ChromeOS" or ffmpeg_branding=="Chrome")', {
              'dependencies': [
                'make_ffmpeg_asm_lib',
              ],
              'sources': [
                'patched-ffmpeg-mt/libavcodec/x86/mpegvideo_mmx.c',
# aug 11                'patched-ffmpeg-mt/libavcodec/x86/h264dsp_mmx.c',

              ],
            }],
            ['(target_arch=="ia32" or target_arch=="x64") and ffmpeg_branding=="ChromeOS"', {
              'dependencies': [
                'make_ffmpeg_asm_lib',
              ],
              'sources': [
                'patched-ffmpeg-mt/libavcodec/x86/vc1dsp_mmx.c',
              ],
            }],
            ['target_arch=="ia32"', {
              'cflags!': [
                # Turn off valgrind build option that breaks ffmpeg builds.
                # Allows config.h HAVE_EBP_AVAILABLE 1 and HAVE_EBX_AVAILABLE 1
                '-fno-omit-frame-pointer',
              ],
            }],  # target_arch=="ia32"
            ['target_arch=="x64"', {
              # x64 requires PIC for shared libraries. This is opposite
              # of ia32 where due to a slew of inline assembly using ebx,
              # FFmpeg CANNOT be built with PIC.
              'defines': [
                'PIC',
              ],
              'cflags': [
                '-fPIC',
              ],
            }],  # target_arch=="x64"
            ['target_arch=="arm"', {
              'defines': [
                'PIC',
              ],
              'cflags': [
                '-fPIC',
              ],
              'sources': [
                'patched-ffmpeg-mt/libavcodec/arm/dsputil_arm.S',
                'patched-ffmpeg-mt/libavcodec/arm/dsputil_armv6.S',
                'patched-ffmpeg-mt/libavcodec/arm/dsputil_init_arm.c',
                'patched-ffmpeg-mt/libavcodec/arm/dsputil_init_armv5te.c',
                'patched-ffmpeg-mt/libavcodec/arm/dsputil_init_armv6.c',
                'patched-ffmpeg-mt/libavcodec/arm/dsputil_init_vfp.c',
                'patched-ffmpeg-mt/libavcodec/arm/dsputil_vfp.S',
                'patched-ffmpeg-mt/libavcodec/arm/fft_init_arm.c',
                'patched-ffmpeg-mt/libavcodec/arm/jrevdct_arm.S',
                'patched-ffmpeg-mt/libavcodec/arm/simple_idct_arm.S',
                'patched-ffmpeg-mt/libavcodec/arm/simple_idct_armv5te.S',
                'patched-ffmpeg-mt/libavcodec/arm/simple_idct_armv6.S',
              ],
              # TODO(scherkus): Temporary until libvpx compiles on ARM.
              'sources!': [
                'patched-ffmpeg-mt/libavcodec/libvpxdec.c',
              ],
              'conditions': [
                ['arm_neon==1', {
                  'sources': [
                    'patched-ffmpeg-mt/libavcodec/arm/dsputil_init_neon.c',
                    'patched-ffmpeg-mt/libavcodec/arm/dsputil_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/fft_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/int_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/rdft_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/simple_idct_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/vp3dsp_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/mdct_neon.S',
                  ],
                }],
              ],
            }],  # target_arch=="arm"
            ['target_arch=="arm" and (ffmpeg_branding=="Chrome" or ffmpeg_branding=="ChromeOS")', {
              'sources': [
                'patched-ffmpeg-mt/libavcodec/arm/h264dsp_init_arm.c',
                'patched-ffmpeg-mt/libavcodec/arm/h264pred_init_arm.c',
                'patched-ffmpeg-mt/libavcodec/arm/mpegvideo_arm.c',
                'patched-ffmpeg-mt/libavcodec/arm/mpegvideo_armv5te.c',
                'patched-ffmpeg-mt/libavcodec/arm/mpegvideo_armv5te_s.S',
              ],
              'conditions': [
                ['arm_neon==1', {
                  'sources': [
                    'patched-ffmpeg-mt/libavcodec/arm/h264dsp_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/h264idct_neon.S',
                    'patched-ffmpeg-mt/libavcodec/arm/h264pred_neon.S',
                  ],
                }],
              ],
            }],
            ['OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="solaris"', {
              'defines': [
                '_ISOC99_SOURCE',
                '_LARGEFILE_SOURCE',
              ],
              'cflags': [
                '-std=c99',
                '-pthread',
                '-fno-math-errno',
              ],
              'cflags!': [
                # Ensure the symbols are exported.
                #
                # TODO(ajwong): Fix common.gypi to only add this flag for
                # _type != shared_library.
                '-fvisibility=hidden',
              ],
              'link_settings': {
                'ldflags': [
                  '-Wl,-Bsymbolic',
                  '-L<(shared_generated_dir)',
                ],
                'libraries': [
                  '-lz',
                ],
                'conditions': [
                  ['target_arch!="arm"', {
                    'libraries': [
                      # TODO(scherkus): Temporary until libvpx compiles on ARM.
                      '-lvpx',
                    ],
                  }],
                  ['ffmpeg_asm_lib==1', {
                    'libraries': [
                      # TODO(ajwong): When scons is dead, collapse this with the
                      # absolute path entry inside the OS="mac" conditional, and
                      # move it out of the conditionals block altogether.
                      '-l<(asm_library)',
                    ],
                  }],
                  ['use_system_vpx==0', {
                    'ldflags': [
                      '-L<(libvpx_hack_dir)/lib/<(OS)/<(target_arch)',
                    ],
                  }],
                ],
              },
            }],  # OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="solaris"
            ['OS=="mac"', {
              'libraries': [
                # TODO(ajwong): Move into link_settings when this is fixed:
                #
                # http://code.google.com/p/gyp/issues/detail?id=108
                '<(shared_generated_dir)/<(STATIC_LIB_PREFIX)<(asm_library)<(STATIC_LIB_SUFFIX)',
                '<(libvpx_hack_dir)/lib/<(OS)/<(target_arch)/libvpx.a',
              ],
              'link_settings': {
                'libraries': [
                  '$(SDKROOT)/usr/lib/libz.dylib',
                ],
              },
              'xcode_settings': {
                'GCC_SYMBOLS_PRIVATE_EXTERN': 'NO',  # No -fvisibility=hidden
                'GCC_DYNAMIC_NO_PIC': 'YES',         # -mdynamic-no-pic
                                                     # (equiv -fno-PIC)
                'DYLIB_INSTALL_NAME_BASE': '@loader_path',
                'LIBRARY_SEARCH_PATHS': [
                  '<(shared_generated_dir)'
                ],
                'OTHER_LDFLAGS': [
                  # This is needed because FFmpeg cannot be built as PIC, and
                  # thus we need to instruct the linker to allow relocations
                  # for read-only segments for this target to be able to
                  # generated the shared library on Mac.
                  #
                  # This makes Mark sad, but he's okay with it since it is
                  # isolated to this module. When Mark finds this in the
                  # future, and has forgotten this conversation, this comment
                  # should remind him that the world is still nice and
                  # butterflies still exist...as do rainbows, sunshine,
                  # tulips, etc., etc...but not kittens. Those went away
                  # with this flag.
                  '-Wl,-read_only_relocs,suppress',
                  '-L<(libvpx_hack_dir)/lib/mac/ia32'
                ],
              },
            }],  # OS=="mac"
            ['use_system_vpx==0', {
                'include_dirs': [
                  '<(libvpx_incl_dir)',
                ],
              }, {
                # Using libvpx provided by the system.
                'include_dirs': [
                  '/usr/include/vpx',
                ],
              }
            ],
          ],
          'actions': [
            {
              # Needed to serialize the output of make_ffmpeg_asm_lib with
              # this target being built.
              'action_name': 'ffmpegasm_barrier',
              'inputs': [
                '<(shared_generated_dir)/<(STATIC_LIB_PREFIX)<(asm_library)<(STATIC_LIB_SUFFIX)',
              ],
              'outputs': [
                '<(INTERMEDIATE_DIR)/third_party/ffmpeg/<(asm_library)'
              ],
              'action': [
                'touch',
                '<(INTERMEDIATE_DIR)/third_party/ffmpeg/<(asm_library)'
              ],
              'process_outputs_as_sources': 0,
              'message': 'Serializing build of <(asm_library).',
            },
          ],
        },
        {
          'target_name': 'assemble_ffmpeg_asm',
          'type': 'none',
          'conditions': [
            ['use_system_yasm==0', {
              'dependencies': [
                '../yasm/yasm.gyp:yasm#host',
              ],
              'variables': {
                'yasm_path': '<(PRODUCT_DIR)/yasm',
              },
            },{  # use_system_yasm!=0
              'variables': {
                'yasm_path': '<!(which yasm)',
              },
            }],
          ],
          'sources': [
            # The FFmpeg yasm files.
            'patched-ffmpeg-mt/libavcodec/x86/deinterlace.asm',  # aug 11
            'patched-ffmpeg-mt/libavcodec/x86/dsputil_yasm.asm',
            'patched-ffmpeg-mt/libavcodec/x86/fft_mmx.asm',
            'patched-ffmpeg-mt/libavcodec/x86/h264_deblock_sse2.asm',  # aug 11
            'patched-ffmpeg-mt/libavcodec/x86/h264_intrapred.asm',  # new
            'patched-ffmpeg-mt/libavcodec/x86/h264_weight_sse2.asm',  # aug 11
	    'patched-ffmpeg-mt/libavcodec/x86/vc1dsp_yasm.asm',  # new
          ],
          'rules': [
            {
              'conditions': [
                ['OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="solaris"', {
                  'variables': {
                    'obj_format': 'elf',
                  },
                  'conditions': [
                    ['target_arch=="ia32"', {
                      'variables': {
                        'yasm_flags': [
                          '-DARCH_X86_32',
                          '-m', 'x86',
                        ],
                      },
                    }],
                    ['target_arch=="x64"', {
                      'variables': {
                        'yasm_flags': [
                          '-DARCH_X86_64',
                          '-m', 'amd64',
                          '-DPIC',
                        ],
                      },
                    }],
                    ['target_arch=="arm"', {
                      'variables': {
                        'yasm_flags': [],
                      },
                    }],
                  ],
                }], ['OS=="mac"', {
                  'variables': {
                    'obj_format': 'macho',
                    'yasm_flags': [ '-DPREFIX', ],
                  },
                  'conditions': [
                    ['target_arch=="ia32"', {
                      'variables': {
                        'yasm_flags': [
                          '-DARCH_X86_32',
                          '-m', 'x86',
                        ],
                      },
                    }],
                    ['target_arch=="x64"', {
                      'variables': {
                        'yasm_flags': [
                          '-DARCH_X86_64',
                          '-m', 'amd64',
                          '-DPIC',
                        ],
                      },
                    }],
                  ],
                }],
              ],
              'rule_name': 'assemble',
              'extension': 'asm',
              'inputs': [ '<(yasm_path)', ],
              'outputs': [
                '<(shared_generated_dir)/<(RULE_INPUT_ROOT).o',
              ],
              'action': [
                '<(yasm_path)',
                '-f', '<(obj_format)',
                '<@(yasm_flags)',
                '-I', 'patched-ffmpeg-mt/libavcodec/x86/',
                '-o', '<(shared_generated_dir)/<(RULE_INPUT_ROOT).o',
                '<(RULE_INPUT_PATH)',
              ],
              'process_outputs_as_sources': 0,
              'message': 'Build ffmpeg yasm build <(RULE_INPUT_PATH).',
            },
          ],
        },
        {
          'target_name': 'make_ffmpeg_asm_lib',
          'type': 'none',
          'dependencies': [
            'assemble_ffmpeg_asm',
          ],
          'sources': [
          ],
          'actions': [
            {
              'action_name': 'make_library',
              'variables': {
                # Make sure this stays in sync with the corresponding sources
                # in assemble_ffmpeg_asm.
                'asm_objects': [
                  '<(shared_generated_dir)/deinterlace.o',
                  '<(shared_generated_dir)/dsputil_yasm.o',
                  '<(shared_generated_dir)/fft_mmx.o',
                  '<(shared_generated_dir)/h264_deblock_sse2.o',
                  '<(shared_generated_dir)/h264_intrapred.o',
                  '<(shared_generated_dir)/h264_weight_sse2.o',
                  '<(shared_generated_dir)/vc1dsp_yasm.o',
                ],
                'library_path': '<(shared_generated_dir)/<(STATIC_LIB_PREFIX)<(asm_library)<(STATIC_LIB_SUFFIX)',
              },
              'inputs': [ '<@(asm_objects)', ],
              'outputs': [ '<(library_path)', ],
              'action': [ 'ar', 'rcs', '<(library_path)', '<@(asm_objects)', ],
              'process_outputs_as_sources': 0,
              'message': 'Packate ffmpeg assembly into <(library_path).',
            },
          ],
        },
        {
          # A target shim that allows putting a dependency on ffmpegsumo
          # without pulling it into the link line.
          #
          # We use an "executable" taget without any sources to break the
          # link line relationship to ffmpegsumo.
          #
          # Most people will want to depend on this target instead of on
          # ffmpegsumo directly since ffmpegsumo is meant to be
          # used via dlopen() in chrome.
          'target_name': 'ffmpegsumo_nolink',
          'type': 'executable',
          'sources': [ 'dummy_nolink.cc' ],
          'dependencies': [
            'ffmpegsumo',
          ],
          'conditions': [
            ['OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="solaris"', {
              'copies': [
                {
                  # On Make and Scons builds, the library does not end up in
                  # the PRODUCT_DIR.
                  #
                  # http://code.google.com/p/gyp/issues/detail?id=57
                  #
                  # TODO(ajwong): Fix gyp, fix the world.
                  'destination': '<(PRODUCT_DIR)',
                  'files': ['<(SHARED_LIB_DIR)/<(SHARED_LIB_PREFIX)ffmpegsumo<(SHARED_LIB_SUFFIX)'],
                },
              ],
            }],
          ],
        },
      ],
    }],
  ],  # conditions
  'targets': [
    {
      'variables': {
        'generate_stubs_script': '../../tools/generate_stubs/generate_stubs.py',
        'sig_files': [
          # Note that these must be listed in dependency order.
          # (i.e. if A depends on B, then B must be listed before A.)
          'avutil-50.sigs',
          'avcodec-52.sigs',
          'avformat-52.sigs',
        ],
        'extra_header': 'ffmpeg_stub_headers.fragment',
      },

      'target_name': 'ffmpeg',
      'msvs_guid': 'D7A94F58-576A-45D9-A45F-EB87C63ABBB0',
      'sources': [
        # Hacks to introduce C99 types into Visual Studio.
        'include/win/inttypes.h',
        'include/win/stdint.h',

        # Files needed for stub generation rules.
        '<@(sig_files)',
        '<(extra_header)'
      ],
      'defines': [
        '__STDC_CONSTANT_MACROS',  # FFmpeg uses INT64_C.
      ],
      'hard_dependency': 1,

      # Do not fear the massive conditional blocks!  They do the following:
      #   1) Use the Window stub generator on Windows
      #   2) Else, use the POSIX stub generator on non-Windows
      #     a) Use system includes when use_system_ffmpeg!=0
      #     b) Else, use our local copy in patched-ffmpeg-mt
      'conditions': [
        ['OS=="win"', {
          'variables': {
            'outfile_type': 'windows_lib',
            'output_dir': '<(PRODUCT_DIR)/lib',
            'intermediate_dir': '<(INTERMEDIATE_DIR)',
            # TODO(scherkus): Change Windows DEPS directory so we don't need
            # this conditional.
            'conditions': [
              [ 'ffmpeg_branding=="Chrome"', {
                'ffmpeg_bin_dir': 'chrome/<(OS)/<(ffmpeg_variant)',
              }, {  # else ffmpeg_branding!="Chrome", assume chromium.
                'ffmpeg_bin_dir': 'chromium/<(OS)/<(ffmpeg_variant)',
              }],
            ],
          },
          'type': 'none',
          'sources!': [
            '<(extra_header)',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              'include/win',
              'config',
              'patched-ffmpeg-mt',
            ],
            'link_settings': {
              'libraries': [
                '<(output_dir)/avcodec-52.lib',
                '<(output_dir)/avformat-52.lib',
                '<(output_dir)/avutil-50.lib',
              ],
              'msvs_settings': {
                'VCLinkerTool': {
                  'DelayLoadDLLs': [
                    'avcodec-52.dll',
                    'avformat-52.dll',
                    'avutil-50.dll',
                  ],
                },
              },
            },
          },
          'rules': [
            {
              'rule_name': 'generate_libs',
              'extension': 'sigs',
              'inputs': [
                '<(generate_stubs_script)',
                '<@(sig_files)',
              ],
              'outputs': [
                '<(output_dir)/<(RULE_INPUT_ROOT).lib',
              ],
              'action': ['python', '<(generate_stubs_script)',
                         '-i', '<(intermediate_dir)',
                         '-o', '<(output_dir)',
                         '-t', '<(outfile_type)',
                         '<@(RULE_INPUT_PATH)',
              ],
              'message': 'Generating FFmpeg import libraries.',
            },
          ],

          # Copy prebuilt binaries to build directory.
          'dependencies': ['../../build/win/system.gyp:cygwin'],
          'copies': [{
            'destination': '<(PRODUCT_DIR)/',
            'files': [
              'binaries/<(ffmpeg_bin_dir)/avcodec-52.dll',
              'binaries/<(ffmpeg_bin_dir)/avformat-52.dll',
              'binaries/<(ffmpeg_bin_dir)/avutil-50.dll',
            ],
          }],
        }, {  # else OS!="win", use POSIX stub generator
          'variables': {
            'outfile_type': 'posix_stubs',
            'stubs_filename_root': 'ffmpeg_stubs',
            'project_path': 'third_party/ffmpeg',
            'intermediate_dir': '<(INTERMEDIATE_DIR)',
            'output_root': '<(SHARED_INTERMEDIATE_DIR)/ffmpeg',
          },
          'type': '<(library)',
          'include_dirs': [
            '<(output_root)',
            '../..',  # The chromium 'src' directory.
          ],
          'direct_dependent_settings': {
            'defines': [
              '__STDC_CONSTANT_MACROS',  # FFmpeg uses INT64_C.
            ],
            'include_dirs': [
              '<(output_root)',
              '../..',  # The chromium 'src' directory.
            ],
          },
          'actions': [
            {
              'action_name': 'generate_stubs',
              'inputs': [
                '<(generate_stubs_script)',
                '<(extra_header)',
                '<@(sig_files)',
              ],
              'outputs': [
                '<(intermediate_dir)/<(stubs_filename_root).cc',
                '<(output_root)/<(project_path)/<(stubs_filename_root).h',
              ],
              'action': ['python',
                         '<(generate_stubs_script)',
                         '-i', '<(intermediate_dir)',
                         '-o', '<(output_root)/<(project_path)',
                         '-t', '<(outfile_type)',
                         '-e', '<(extra_header)',
                         '-s', '<(stubs_filename_root)',
                         '-p', '<(project_path)',
                         '<@(_inputs)',
              ],
              'process_outputs_as_sources': 1,
              'message': 'Generating FFmpeg stubs for dynamic loading.',
            },
          ],

          'conditions': [
            # Linux/Solaris need libdl for dlopen() and friends.
            ['OS=="linux" or OS=="solaris"', {
              'link_settings': {
                'libraries': [
                  '-ldl',
                ],
              },
            }],

            # Add pkg-config result to include path when use_system_ffmpeg!=0
            ['use_system_ffmpeg!=0', {
              'cflags': [
                '<!@(pkg-config --cflags libavcodec libavformat libavutil)',
              ],
              'direct_dependent_settings': {
                'cflags': [
                  '<!@(pkg-config --cflags libavcodec libavformat libavutil)',
                ],
              },
            }, {  # else use_system_ffmpeg==0, add local copy to include path
              'include_dirs': [
                'config',
                'patched-ffmpeg-mt',
              ],
              'direct_dependent_settings': {
                'include_dirs': [
                  'config',
                  'patched-ffmpeg-mt',
                ],
              },
              'conditions': [
                ['build_ffmpegsumo!=0', {
                  'dependencies': [
                    'ffmpegsumo_nolink',
                  ],
                }],
              ],
            }],
          ],  # conditions
        }],
      ],  # conditions
    },
  ],  # targets
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
