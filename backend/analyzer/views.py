from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import sys
import os

# Add paths
ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ml'))
analyzer_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ml_path)
sys.path.insert(0, analyzer_path)

@csrf_exempt
@require_http_methods(["POST"])
def analyze(request):
    try:
        from url_analyzer import analyze_url
        from domain_checker import check_domain_in_db
        data = json.loads(request.body)
        input_type = data.get('type', 'text')  # text / url / image
        content = data.get('content', '')

        result = {
            'input_type': input_type,
            'content': content[:200],
            'ml_result': None,
            'url_result': None,
            'domain_result': None,
            'final_verdict': 'UNVERIFIED',
            'final_score': 50,
        }

        # URL Analysis
        if input_type == 'url':
            url_result = analyze_url(content)
            domain_result = check_domain_in_db(url_result.get('domain', ''))
            result['url_result'] = url_result
            result['domain_result'] = domain_result
            result['final_score'] = url_result.get('trust_score', 50)
            result['final_verdict'] = url_result.get('verdict', 'UNVERIFIED')

        # Text Analysis using ML
        elif input_type == 'text':
            try:
                import joblib
                import scipy.sparse as sp
                from scipy.sparse import hstack

                models_path = r'D:\TruthCheck\TruthCheck\ml\models'
                tfidf = joblib.load(os.path.join(models_path, 'tfidf.pkl'))
                rf = joblib.load(os.path.join(models_path, 'random_forest.pkl'))

                from preprocess import clean_text
                from features import clickbait_score, emotional_score, punctuation_score, text_length

                cleaned = clean_text(content)
                X_tfidf = tfidf.transform([cleaned])
                extra = sp.csr_matrix([[
                    clickbait_score(content),
                    emotional_score(content),
                    punctuation_score(content),
                    text_length(content)
                ]])
                X = hstack([X_tfidf, extra])
                proba = rf.predict_proba(X)[0]
                verdict = 'REAL' if proba[1] > 0.5 else 'FAKE'
                confidence = round(float(max(proba)) * 100, 2)

                result['ml_result'] = {
                    'verdict': verdict,
                    'confidence': confidence,
                    'fake_probability': round(float(proba[0]) * 100, 2),
                    'real_probability': round(float(proba[1]) * 100, 2),
                }
                result['final_verdict'] = verdict
                result['final_score'] = confidence
            except Exception as e:
                result['ml_error'] = str(e)

        # Final verdict label
        ml = result.get('ml_result')
        if ml:
            if ml['verdict'] == 'FAKE':
                result['final_verdict'] = '❌ LIKELY FAKE'
            else:
                result['final_verdict'] = '✅ LIKELY REAL'
        else:
            score = result['final_score']
            if score >= 75:
                result['final_verdict'] = '✅ LIKELY REAL'
            elif score >= 50:
                result['final_verdict'] = '⚠️ UNVERIFIED'
            else:
                result['final_verdict'] = '❌ LIKELY FAKE'

        return JsonResponse({'success': True, 'result': result})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)