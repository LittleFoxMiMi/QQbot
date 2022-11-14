from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    bilibili_cookie: str = "buvid3=E1363679-C3C6-4A2E-ABEB-25BD8C2A559B34766infoc; LIVE_BUVID=AUTO3416217798242082; video_page_version=v_old_home_18; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; DedeUserID=32953462; DedeUserID__ckMd5=73b09f8b34c1da3d; b_ut=5; _uuid=6E215219-6E7D-EDF9-C3BE-83D731762E10318258infoc; hit-dyn-v2=1; CURRENT_QUALITY=80; nostalgia_conf=-1; blackside_state=0; fingerprint3=4817433298a6a3e7f4d7fc51bb99fd03; PVID=2; b_nut=100; buvid4=113ACBBD-FE41-91C2-DC1A-2FDEAF0573F524773-022022615-GlymH7ZVG/nk4SRA9SUHPQ==; fingerprint=7ef3afef39033fac14cef82a3d41946f; CURRENT_FNVAL=4048; buvid_fp=7ef3afef39033fac14cef82a3d41946f; innersign=0; b_lsid=9AC57426_18474186092; SESSDATA=4dc4e6c6,1683947081,a1610*b2; bili_jct=ba6ef7dadf6fad37335624f5d9b93eee; sid=73pgujm0; bp_video_offset_32953462=728183792233087000"
