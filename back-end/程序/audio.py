import ChatTTS
import soundfile

chat = ChatTTS.Chat()
chat.download_models(source="local")
chat.load(compile=True)

rand_spk = soundfile.get_random_speaker()

params_infer_code = ChatTTS.Chat.InferParams(
    spk_emb=rand_spk,
    temperature=0.3,
    top_k=20,
    top_p=0.7,
)

params_refine_text = ChatTTS.Chat.RefineTextParams(
    prompt='[oral_2][laugh_0][break_6]'
)


def get_wav(text):
    wavs = chat.infer(text, skip_refine_text=True, params_refine_text=params_refine_text, params_infer_code=params_infer_code)
    return wavs[0][0]