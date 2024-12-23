from flask import Flask, request, jsonify, render_template
from catboost import CatBoostClassifier
import numpy as np
import pickle
import pandas as pd
app = Flask(__name__)

# 모델 로드 (pickle을 사용하여 catboost_model.pk1 파일에서 모델 로드)
with open("catboost_model2.pk1", "rb") as file:
    model = pickle.load(file)
def map_travel_style(choice,style):
    mapping={
        'nature_city': {
            'nature': range(1, 4), 
            'city': range(4, 8)    
        },
        'plan_no_plan': {
            'plan': range(1, 4),
            'no-plan': range(4, 8)
        },
        'play_no_play' : {
            'no-play': range(1, 4),
            'play': range(4, 8)
        },
        'photo_memory': {
            'photo': range(4, 8),
            'memory': range(1, 4)
        },
        'famous_discover': {
            'famous': range(4, 8),
            'discover': range(1, 4)
        }
    }
    return sum(mapping[style][choice]) // len(mapping[style][choice])

def test_code(user_choices, user_info):
    results = pd.read_csv('df_final_noarr.csv')  # 데이터프레임 로드

    # traveler 객체 생성
    traveler = {
        'GENDER': int(user_info['gender']),
        'AGE_GRP': float(user_info['age']),
        'TRAVEL_STYL_1': user_choices['nature_city'],
        'TRAVEL_STYL_2': user_choices['play_no_play'],
        'TRAVEL_STYL_5': user_choices['play_no_play'],
        'TRAVEL_STYL_6': user_choices['famous_discover'],
        'TRAVEL_STYL_7': user_choices['plan_no_plan'],
        'TRAVEL_STYL_8': user_choices['photo_memory'],
        'VISIT_ORDER': 13
    }
    
    # traveler = {
    # 'GENDER': 0,
    # 'AGE_GRP': 40.0,
    # 'TRAVEL_STYL_1': 1,
    # 'TRAVEL_STYL_2': 2,
    # 'TRAVEL_STYL_5': 2,
    # 'TRAVEL_STYL_6': 4,
    # 'TRAVEL_STYL_7': 2,
    # 'TRAVEL_STYL_8': 4,
    # 'VISIT_ORDER': 13
    # }

    # traveler 객체를 콘솔에 출력
    print("Traveler 객체 구성:", traveler)
    
    print(results.head())

    # traveler 객체를 이용해 결과 필터링
    filtered_results = results[
        (results['GENDER'] == traveler['GENDER']) &
        (results['AGE_GRP'] == traveler['AGE_GRP']) &
        (results['TRAVEL_STYL_1'] == traveler['TRAVEL_STYL_1']) &
        # (results['TRAVEL_STYL_2'] == traveler['TRAVEL_STYL_2']) &
        (results['TRAVEL_STYL_5'] == traveler['TRAVEL_STYL_5'])&
        (results['TRAVEL_STYL_6'] == traveler['TRAVEL_STYL_6']) 
        # (results['TRAVEL_STYL_7'] == traveler['TRAVEL_STYL_7']) 
        # (results['TRAVEL_STYL_8'] == traveler['TRAVEL_STYL_8'])
    ]

    # 필터링된 결과가 없으면 빈 결과를 반환
    if filtered_results.empty:
        print("필터링된 결과가 없습니다.")
        return pd.DataFrame([], columns=['VISIT_AREA_NM', 'SCORE'])

    # 결과 데이터프레임을 초기화하고 모델 예측 수행
    results = pd.DataFrame([], columns=['VISIT_AREA_NM', 'SCORE'])

    for area in filtered_results['VISIT_AREA_NM']:
        input_df = list(traveler.values())
        input_df.append(area)

        print(input_df)
        score = model.predict(input_df)  # 입력값을 리스트로 감싸서 전달
        print([area, score])
        results= pd.concat([results, pd.DataFrame([[area, score]], columns=['VISIT_AREA_NM', 'SCORE'])])

    if results.empty:
        print("결과를 계산할 수 없습니다.")
        return pd.DataFrame([], columns=['VISIT_AREA_NM', 'SCORE'])

    #중복제거
    results = results.drop_duplicates(keep='first')
    
    top_area = results.sort_values('SCORE', ascending=False)[:10]
    top_area['SCORE'] = top_area['SCORE'].round(2)
    print(top_area)
    return top_area


    
# from flask import Flask, request, jsonify, render_template
# from catboost import CatBoostClassifier
# import numpy as np
# import pickle
# import pandas as pd
# app = Flask(__name__)

# 모델 로드 (pickle을 사용하여 catboost_model.pk1 파일에서 모델 로드)
# with open("catboost_model2.pk1", "rb") as file:
#     model = pickle.load(file)
# def map_travel_style(choice,style):
#     mapping={
#         'nature_city': {
#             'nature': range(1, 5), 
#             'city': range(5, 11)    
#         },
#         'plan_no_plan': {
#             'plan': range(1, 5),
#             'no-plan': range(5, 11)
#         },
#         'play_no_play' : {
#             'no-play': range(1,5),
#             'play': range(5,11)
#         },
#         'photo_memory': {
#             'memory': range(1,5),
#             'photo': range(5, 11)
#         },
#         'famous_discover': {
#             'discover': range(1, 5),
#             'famous': range(5,11)
#         }
#     }
#     return sum(mapping[style][choice]) // len(mapping[style][choice])

# def test_code(user_choices, user_info):
#     results = pd.read_csv('df_final.csv')

#     traveler = {
#         'GENDER': int(user_info['gender']),
#         'AGE_GRP': float(user_info['age']),
#         'TRAVEL_STYL_1': map_travel_style(user_choices['nature_city'], 'nature_city'),
#         'TRAVEL_STYL_5': map_travel_style(user_choices['play_no_play'], 'play_no_play'),
#         'TRAVEL_STYL_6': map_travel_style(user_choices['famous_discover'], 'famous_discover'),
#         'TRAVEL_STYL_7': map_travel_style(user_choices['plan_no_plan'], 'plan_no_plan'),
#         'TRAVEL_STYL_8': map_travel_style(user_choices['photo_memory'], 'photo_memory'),
#         'VISIT_ORDER': 13
#     }
    
#     print("Traveler 객체 구성:", traveler)

#     # 단계별로 필터링
#     # step1 = results[results['GENDER'] == traveler['GENDER']]
#     # step2 = step1[step1['AGE_GRP'] == traveler['AGE_GRP']]
#     # step3 = step2[step2['TRAVEL_STYL_1'] == traveler['TRAVEL_STYL_1']]
#     # step4 = step3[step3['TRAVEL_STYL_5'] == traveler['TRAVEL_STYL_5']]
#     # step5 = step4[step4['TRAVEL_STYL_6'] == traveler['TRAVEL_STYL_6']]
#     # step6 = step5[step5['TRAVEL_STYL_7'] == traveler['TRAVEL_STYL_7']]
#     # filtered_results = step6[step6['TRAVEL_STYL_8'] == traveler['TRAVEL_STYL_8']]

#     # 각 단계에서의 필터링 결과를 확인
#     # print(f"Step 1 (GENDER) 결과 수: {len(step1)}")
#     # print(f"Step 2 (AGE_GRP) 결과 수: {len(step2)}")
#     # print(f"Step 3 (TRAVEL_STYL_1) 결과 수: {len(step3)}")
#     # print(f"Step 4 (TRAVEL_STYL_5) 결과 수: {len(step4)}")
#     # print(f"Step 5 (TRAVEL_STYL_6) 결과 수: {len(step5)}")
#     # print(f"Step 6 (TRAVEL_STYL_7) 결과 수: {len(step6)}")
#     # print(f"최종 필터링된 결과 수: {len(filtered_results)}")

#     if filtered_results.empty:
#         print("필터링된 결과가 없습니다.")
#         return pd.DataFrame([], columns=['VISIT_AREA_NM', 'SCORE'])

#     # 필터링된 결과를 사용하여 예측 수행
#     results_df = pd.DataFrame([], columns=['VISIT_AREA_NM', 'SCORE'])

#     for area in filtered_results['VISIT_AREA_NM']:
#         input_data = list(traveler.values())
#         input_data.append(area)

#         score = model.predict([input_data])
#         print([area, score])
#         results_df = pd.concat([results_df, pd.DataFrame([[area, score]], columns=['VISIT_AREA_NM', 'SCORE'])])

#     if results_df.empty:
#         print("결과를 계산할 수 없습니다.")
#         return pd.DataFrame([], columns=['VISIT_AREA_NM', 'SCORE'])

#     top_area = results_df.sort_values('SCORE', ascending=False).head(10)
#     print(top_area)
#     return top_area


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # JSON 요청에서 데이터 가져오기
        data = request.json
        print(data)
        # user_info와 user_choices 추출
        user_info = {
            'age': data.get('age'),
            'gender': data.get('gender')
        }
        
        user_choices = {
            'nature_city': data.get('nature_city'),
            'plan_no_plan': data.get('plan_no_plan'),
            'play_no_play': data.get('play_no_play'),
            'photo_memory': data.get('photo_memory'),
            'famous_discover': data.get('famous_discover')
        }
        print(user_info)
        print(user_choices)
        mapped_choices = {key: map_travel_style(value, key) for key, value in user_choices.items()}
        print("Mapped Choices:", mapped_choices)
        # test_code 함수 호출
        df = test_code(mapped_choices, user_info)
        
        # DataFrame을 JSON으로 변환하여 반환
        df_json = df.to_json(orient='records', force_ascii=False)

        # traveler 객체와 예측 결과를 함께 반환
        # return jsonify({'prediction': df_json})
        return jsonify(df_json)
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return jsonify({'error': '서버 내부 오류가 발생했습니다.'}), 500



@app.route('/test-first', methods=['GET'])
def test_first():
    # index.html 파일을 렌더링
    return render_template('test-first.html')

@app.route('/', methods=['GET'])
def first():
    # index.html 파일을 렌더링
    return render_template('first.html')

@app.route('/index', methods=['GET'])
def index():
    # index.html 파일을 렌더링
    return render_template('index.html')


@app.route('/result.html', methods=['GET'])
def result():
    # result.html 파일을 렌더링
    return render_template('result.html')

if __name__ == '__main__':    
    app.run(debug=True, port=5500)

@app.route('/test-first', methods=['GET'])
def test_first():
    # index.html 파일을 렌더링
    return render_template('test-first.html')

@app.route('/', methods=['GET'])
def first():
    # index.html 파일을 렌더링
    return render_template('first.html')

@app.route('/index', methods=['GET'])
def index():
    # index.html 파일을 렌더링
    return render_template('index.html')


@app.route('/result.html', methods=['GET'])
def result():
    # result.html 파일을 렌더링
    return render_template('result.html')

if __name__ == '__main__':    
    app.run(debug=True, port=5500)
