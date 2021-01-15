import pandas as pd
import glob
import reportgenerator.Tools as tools
from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from math import pi
import numpy as np
import os
import shutil
import math

plt.rcParams['font.family'] = 'Noto Sans CJK JP'

class ResourceManager():
    filecount = 0
    WORK_DIR: str

    def __init__(self, template_path: str, report_dataset: dict):
        self.opinionfile = '000-Opinion.txt'
        self.TEMPLATE_PATH = template_path
        self.report_dataset = report_dataset

    def make_summary_result(self, workdir_path: str, summarydir_path: str, summaryfile_path: str):
        # サマリ用のレーダーチャートを作成し、SUMMARYディレクトリに格納する
        try:
            print('ResourceManager() make_summary_result() start')
            if not (os.path.exists(summarydir_path)):
                os.makedirs(summarydir_path)

            shutil.copyfile(self.TEMPLATE_PATH + "frame_summary.html",
                            summaryfile_path)
            self.__make_summary_radarchart(summarydir_path)  # レーダーチャート作成
            self.__make_summary_overview(summarydir_path)
        except Exception as e:
            raise e
        return 0

    def __make_summary_overview(self, summarydir_path: str):
        # 数値目標(ValueTarget)の有無を判定し、有のTDに関しては、目標達成か否か(TestDescriptionResult)も判定
        # 3色グラフで品質目標達成/未達/非該当を描画

        # 内部品質ごとにテスト目標達成度をカウント
        try:
            df_overview = pd.DataFrame(columns=["目標達成", "目標未達成", "非該当"])
            for qp_id, qp_category in self.report_dataset['QualityDimension'].items():

                qp_category = '\n'.join(textwrap.wrap(qp_category, 20))

                cnt_pass = 0
                cnt_fail = 0
                cnt_noentry = 0

                # TDが存在しない
                if self.report_dataset['TestDescriptionDetail'] is None:
                    s = pd.Series([0, 0, 0], index=df.columns, name=qp_item)
                    df_overview = df_overview.append(s)
                    continue

                for td_id in self.report_dataset['TestDescriptionDetail'].keys():
                    td_data = self.report_dataset['TestDescriptionDetail'][td_id]

                    # 内部品質特性に属しているか
                    if str(td_data['QualityDimension']['Id']) != str(qp_id):
                        continue
                    # 数値目標設定対象か否か
                    if td_data['ValueTarget'] != 'True':
                        cnt_noentry += 1
                        continue
                    cnt_pass = cnt_pass + 1 if td_data['TestDescriptionResult']["Summary"] == 'OK' else cnt_pass
                    cnt_fail = cnt_fail + 1 if td_data['TestDescriptionResult']["Summary"] != 'OK' else cnt_fail

                # 該当品質特性にTDがない場合、表示対象に含めない
                if cnt_pass == 0 and cnt_fail == 0 and cnt_noentry == 0:
                    continue

                s = pd.Series([cnt_pass, cnt_fail, cnt_noentry], index=df_overview.columns, name=qp_category)
                df_overview = df_overview.append(s)

            # 描画
            plot_df = df_overview.T
            qp_categories = plot_df.columns

            xmax = 0
            for column_name, item in df_overview.iterrows():
                xmax = item.sum() if xmax < item.sum() else xmax
            xmax = xmax + 10  # グラフ横軸 = 最大出力値 + 10

            colorlist = ['blue', 'red', 'lightgray']  # 'pass', 'fail', 'noentry'

            fig, ax = plt.subplots()
            fig.set_figwidth(10.0)
            fig.set_figheight(5.0)
            fig.subplots_adjust(left=0.2)  # y軸に品質特性名を出すためにグラフを左にずらす(表示領域を確保)

            data_points = np.arange(len(qp_categories))
            left_data = pd.Series(np.zeros(len(qp_categories)), index=qp_categories.tolist())

            for i in range(len(plot_df.index)):  # pass,fail,noentry
                bar_list = ax.barh(qp_categories, plot_df.iloc[i],
                                   left=left_data,
                                   linewidth=0.5)
                for j in range(len(bar_list)):
                    bar_list[j].set_facecolor(colorlist[i])
                left_data += plot_df.iloc[i]

            # 凡例
            ax.legend(plot_df.index.tolist(),
                      loc="upper center",
                      ncol=5,
                      bbox_to_anchor=(0.5, 1),
                      frameon=False,
                      borderaxespad=-2,
                      columnspacing=3.5)

            ax.set_yticks(data_points)
            ax.set_xlim([0, xmax])
            ax.set_yticklabels(qp_categories)
            ax.set_xlabel("品質目標が設定されたTestDescription件数")
            plt.savefig(summarydir_path + 'overview.png', dpi=100)

            # Figureウィンドウを閉じる
            plt.close()
        except Exception as e:
            raise e

    def __make_summary_radarchart(self, summarydir_path: str):
        # 内部品質ごとにテスト実施数をカウント
        try:
            values = []
            categories = []

            if self.report_dataset['TestDescriptionDetail'] is None:
                for qp_id in self.report_dataset['QualityDimension'].keys():
                    values += [0]
                    categories = list(value for value in self.report_dataset['QualityDimension'].values())
            else:
                for qp_id in self.report_dataset['QualityDimension'].keys():
                    cnt = 0
                    for td_id in self.report_dataset['TestDescriptionDetail'].keys():
                        qp_td_id = self.report_dataset['TestDescriptionDetail'][td_id]['QualityDimension']['Id']
                        cnt = cnt + 1 if str(qp_td_id) == str(qp_id) else cnt

                    if cnt != 0:
                        values += [cnt]
                        categories.append(self.report_dataset['QualityDimension'][qp_id])

            categories = ['\n'.join(textwrap.wrap(c, 20)) for c in categories]

            N = len(categories)

            if N >= 3:
                # カテゴリ数に合わせて角度を決定
                angles = [n / float(N) * 2 * pi for n in range(N)]
                angles += angles[:1]
            elif N == 2:
                # カテゴリ数が2の場合は、0度と180度で直線になってしまうので、90度にした上でダミーポイントを追加して三角形にする
                angles = [0, 0.5 * np.pi, 0, 0]
                categories += [""] #ダミーのカテゴリ
                values += [0] #ダミーのvalues
            elif N == 1:
                # カテゴリ数が1の場合は、0度だけで点になってしまうので、ダミーのポイントを追加して直線にする
                angles = [0, 0, 0]
                categories += [""] #ダミーのカテゴリ
                values += [0] #ダミーのvalues

            # レーダーチャートを閉じるために最初の値を再度加える(仕様)
            values += [values[0]]

            # レーダーチャート作成
            ax = plt.subplot(111, polar=True)

            plt.xticks(angles[:-1], categories, color='grey', size=10)
            ax.set_rlabel_position(180)

            # レーダーチャートの表示範囲を、valuesの最大値に従って可変にする
            # valuesの最大値
            max_value = max(values)
            # 表示範囲の最大値（５の倍数にする）
            max_range = (int(max_value / 5) + math.ceil((max_value % 5) / 5)) * 5
            # 表示範囲の配列
            display_range_list = np.linspace(0, max_range, 6, dtype = 'int')
            plt.yticks(display_range_list, display_range_list, color="grey", size=10)
            plt.ylim(0, max_range)

            # Plot
            ax.plot(angles, values, linewidth=1, c='m', linestyle='solid')
            ax.fill(angles, values, 'r', alpha=0.2)
            plt.savefig(summarydir_path + 'summary.png', dpi=100)

            # Figureウィンドウを閉じる
            plt.close()
        except Exception as e:
            raise e
        return 0

    # 内部品質ディレクトリ単位のhtmlを作成する
    def make_testdescription_result(self, workdir_path: str):
        # アクセス権限がなかったとき（ファイルが編集中とか）のふるまいをどうするか。
        print('ResourceManager() make_testdescription_result() start')
        try:
            self.WORK_DIR = workdir_path

            # グラフデータが存在しなければ作成しない
            if self.report_dataset['Resources'] is None:
                return

            # メディアファイルのリネーム処理 ← この処理で連番処理でなく、グラフネームにリネームする
            self.rename_mediafile()

            # TDの各メディアファイルで{表示順}-{グラフ名}.htmlを作成する
            resources = self.report_dataset['Resources']
            td_dir_list = []
            for resource in resources:
                qd = resource.get("QualityDimensionId")
                td = resource.get("TD")
                pattern = resource.get('Order') + '-*'
                td_dir_list.append(Path(self.WORK_DIR + qd + os.sep + td + os.sep))
                file_path = list(td_dir_list[-1].glob(pattern))
                # Opinionはスキップする
                if str(file_path[0].name) == self.opinionfile:
                    continue
                if file_path[0].suffix.lower() in {'.csv', '.tsv'}:
                    self.make_table(file_path[0])
                elif file_path[0].suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                    self.make_picture(file_path[0])
                elif file_path[0].suffix.lower() in {'.txt'}:
                    self.make_document(file_path[0])
                else:
                    pass
            # TD単位のHTMLを作成
            td_dir_list = set(td_dir_list)
            for td_dir in td_dir_list:
                self.make_frame_html(td_dir)
        except Exception as e:
            raise e
        return 0

    # CSVファイルをiframeに埋め込んだHTMLを作成する
    def make_table(self, file: Path):
        try:
            htmltable = ""
            number, caption = self.divide_no_and_name(file)
            # csvを<table>に変更。htmlファイルとして出力
            df_s = pd.read_csv(file)
            tableoption = ""
            htmltable += "<table id=\"" + file.stem + "\"" + str(tableoption) + "><tr>"

            for c in df_s.columns.values:
                htmltable += "<th>" + str(c) + "</th>"
            htmltable += "</tr>"

            for index, row in df_s.iterrows():
                htmltable += "<tr>"
                for df in df_s.columns:
                    htmltable += "<th>" + str(row[df]) + "</th>"
                htmltable += "</tr>"

            # TODO 表名前を文字数で折り返すかどうかの判定
            htmltable += "<caption><nobr>Fig." + number + " " + caption + "</nobr></caption></table><br>"

            tools.replace_html(
                self.TEMPLATE_PATH + "frame_table.html",
                htmltable,
                str(file.parent) + os.sep + file.stem + "_table.html",
                "<!--%%TABLE%%-->")
        except Exception as e:
            raise e

    # txtファイルをiframeに埋め込んだHTMLを作成する
    def make_document(self, file: Path):
        # 読み込んだファイルがHTML形式とかjavascriptとかだった場合の対処が必要？
        try:
            htmltextarea = ""
            number, caption = self.divide_no_and_name(file)

            # TODO 折り返し文字数の最大値を定義するが、ゆくゆくは全角半角で最大値を自動調整できるようにする。
            max_folding_len = 70
            f = tools.read_file(file)
            font_type = "style='width:100%; margin: 0px 0px; border:none; overflow:hidden;'"
            htmltextarea += "<figure id=\"" + file.stem + "\"><pre " + font_type + ">"
            lines = [f[i: i + max_folding_len] for i in range(0, len(f), max_folding_len)]
            for line in lines:
                htmltextarea += str(line) + '\r'

            # TODO 表名前を文字数で折り返すかどうかの判定
            htmltextarea += "<figcaption>Fig." + number + " " + caption + "</figcaption></pre></figure><br>\n"

            tools.replace_html(
                self.TEMPLATE_PATH + "frame_textarea.html",
                htmltextarea,
                str(file.parent) + os.sep + file.stem + "_document.html",
                "<!--%%TEXTAREA%%-->")
        except Exception as e:
            raise e

    # ファイルをiframeに埋め込んだHTMLを作成する
    def make_picture(self, file: Path):
        try:
            html_img = ""
            number, caption = self.divide_no_and_name(file)
            html_img += "<figure id=\"" + file.stem + "\"><img src=" + file.name + " alt=" + str(file.name)\
                        + "><figcaption>Fig." + number + " " + caption + "</figcaption></figure><br>\n"
            tools.replace_html(
                self.TEMPLATE_PATH + "frame_image.html",
                html_img,
                str(file.parent) + os.sep + file.stem + "_picture.html",
                "<!--%%IMAGE%%-->")
        except Exception as e:
            raise e

    def __get_uniqueNumber(self):
        self.filecount += 1
        return str(self.filecount)

    # TD内のファイルを{表示順}-{グラフ名}.xxxでリネームする
    def rename_mediafile(self):
        try:
            resources = self.report_dataset['Resources']
            for resource in resources:
                qd = resource.get("QualityDimensionId")
                order = resource.get("Order")
                td = resource.get("TD")
                name = resource.get("Name")
                file = resource.get("File")
                td_path = Path(self.WORK_DIR + qd + os.sep + td + os.sep)
                file_pre_path = Path(os.path.join(td_path, Path(file)))
                file_post_path = Path(os.path.join(td_path, Path(str(order) + '-' + name + file_pre_path.suffix)))
                os.rename(str(file_pre_path), file_post_path)
        except Exception as e:
            raise e

    # TD単位のhtmlを作成する
    def make_frame_html(self, output_path: Path):
        # TD_RESOURCES置換
        output_file = str(output_path.parent) + os.sep + str(output_path.name) + ".html"
        result_iframe = ""
        html_list = glob.glob(str(output_path) + os.sep + "*.html")
        html_list.sort()
        for html_file in html_list:
            path = Path(html_file)
            relative_path = str(path.relative_to(path.parent.parent))
            result_iframe += \
                "<iframe id=\"" + path.stem + "\" onLoad=\"adjust_frame_css(this.id)\" src=\""\
                + relative_path + "\" scrolling=\"no\" frameborder=\"0\" class=\"result_frame\" ></iframe>\n"
        tools.replace_html(
            self.TEMPLATE_PATH + "frame.html",
            result_iframe,
            output_file,
            "<!--%%TD_RESOURCES%%-->",
        )

        # TD_OPINION置換
        opinion_path = os.path.join(Path(output_path.parent), output_path.name, Path(self.opinionfile))
        if Path(opinion_path).exists():
            f = tools.read_file(opinion_path)
        else:
            f = ''
        tools.replace_html(
            output_file,
            f,
            output_file,
            "<!--%%TD_OPINION%%-->",
        )

        # TD_xxx置換
        # TestDescriptionDetailが存在しなければ置き換えない
        if self.report_dataset['TestDescriptionDetail'] is None:
            return

        test_descriptions = self.report_dataset['TestDescriptionDetail']
        td = test_descriptions[output_path.name]

        # TD_NAME
        html_code = 'None' if td['Name'] is None else td['Name']
        tools.replace_html(
            output_file,
            html_code,
            output_file,
            "<!--%%TD_NAME%%-->",
        )
        # TD_INFOMATION
        duplicate_confirmation = []
        html_code = ''
        for qm in td['QualityMeasurements']:
            if qm['Id'] in duplicate_confirmation:
                continue
            html_code += 'None' if qm['Description'] is None else "<li>" + qm['Description'] + "</li>"
            duplicate_confirmation.append(qm['Id'])
        tools.replace_html(
            output_file,
            html_code,
            output_file,
            "<!--%%TD_INFOMATION%%-->",
        )
        # TD_RESULT
        html_code = 'None' if td['TestDescriptionResult'] is None else td['TestDescriptionResult']['Summary']
        if html_code == 'OK':
            html_code = '<span class=\"pass\">pass</span>'
        elif html_code == 'None':
            html_code == 'undecidable'
        else:
            html_code = '<span class=\"fail\">failure</span>'
        tools.replace_html(
            output_file,
            html_code,
            output_file,
            "<!--%%TD_RESULT%%-->",
        )
        # TD_CONDITIONAL_EXPRESSION
        html_code = ''
        for qm in td['QualityMeasurements']:
            html_code += qm['Name'] + qm['RelationalOperator'] + qm['Value'] + ' & '
        html_code = html_code[0:len(html_code) - 2]
        tools.replace_html(
            output_file,
            html_code,
            output_file,
            "<!--%%TD_CONDITIONAL_EXPRESSION%%-->",
        )

        # AIT_NAME
        tools.replace_html(
            output_file,
            td['TestRunner']['Name'],
            output_file,
            "<!--%%AIT_NAME%%-->",
        )
        # AIT_VERSION
        tools.replace_html(
            output_file,
            td['TestRunner']['Version'],
            output_file,
            "<!--%%AIT_VERSION%%-->",
        )
        # AIT_INFOMATION
        tools.replace_html(
            output_file,
            td['TestRunner']['Description'],
            output_file,
            "<!--%%AIT_INFOMATION%%-->",
        )
        # AIT_URL
        tools.replace_html(
            output_file,
            td['TestRunner']['LandingPage'],
            output_file,
            "<!--%%AIT_URL%%-->",
        )

    def divide_no_and_name(self, file: Path):
        if not file.exists():
            return None
        name = file.stem
        number = str(int(name[: name.find('-')]))
        caption = name[name.find('-') + 1:]
        return number, caption
