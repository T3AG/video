import benchmark_ibm_s2t
import benchmark_google_cloudvision

# Path directories
paths = {
    'data_path'         : '../../s3/FF-Data/',
    'ibm_path'          : '!data/benchmark_ibm_',
    'google_path'       : '!data/benchmark_google_',
    'google_auth_path'  : '../auth/benchmark_google_admin_account.json',
    'auth_path'         : '../auth/auth.json'
}

no_videos = 1


benchmark_ibm_s2t.get_return(no_videos, paths)
benchmark_google_cloudvision.get_return(no_videos, paths)

