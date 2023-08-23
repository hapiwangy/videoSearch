
from flask import Flask, render_template, request, redirect, url_for
from diff_functions import setOptions, VideoSearchApi, VideoandUrl



# 設定值和query對應
names = setOptions()
# 設定影片和2對應的URL
vandU = VideoandUrl()

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def root():
    options = setOptions()
    # print(vandU)
    sequence = {}
    NameandTag = {'fence_people':[], 'fence_dog':[], "dock_cargo":[], "AI_360":[]}
    if request.method == 'POST':
        threshold = float(request.form.get('inputNumber'))
        selected_options = request.form.getlist('checkbox')
        ownqueryText = request.form.get('querytextInput')
        # input_number是設定threshold、selected_options設定要被查詢的項目
        if ownqueryText:
            ownqueryText = ownqueryText.split(',')
        if 'selectALLoptions' in ownqueryText:
            Query = list(names.values())
        else:
            Query = [names[x] for x in selected_options]
            for oqT in ownqueryText:
                Query.append(oqT)
        sequence = VideoSearchApi(threshold=float(threshold), query=Query)
        
        # 讓圖片有特定的tag
        for x, y in sequence.items():
            for n, t in NameandTag.items():
                if n in list(y.keys()):
                    t.append(x)
        additional_info = sequence
        # sequence
        ## {tag: {video_name:[{documentId(video_name), start, end, best},...], video_name2}}
        # for k, v in vandU.items():
        #     for y in NameandTag[k]:
        #         for v in additional_info[y][k]:
        #             print(v)
        return render_template("index.html", options = options, NameandTag=NameandTag, vandU=vandU, additional_info = additional_info)
    return render_template("index.html", options = options, NameandTag=NameandTag, vandU = vandU)


if __name__ == '__main__':
    app.run(debug=True)
