// index.html의 '분석하기' 버튼 클릭 시 실행
async function startAnalysis() {
    const url = document.getElementById("url_input").value;
    const openai_key = document.getElementById("openai_key_input").value;
    const sapling_key = document.getElementById("sapling_key_input").value;

    if (!url || !openai_key || !sapling_key) {
        alert("모든 필드를 입력해주세요!");
        return;
    }

    // 로딩 화면으로 즉시 전환
    document.getElementById('main-container').style.display = 'none';
    const loadingContainer = document.getElementById('loading-container');
    loadingContainer.style.display = 'flex';
    
    animateLoadingBarTo99();

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, openai_key, sapling_key })
        });

        const resultData = await response.json();

        const bar = document.getElementById('bar');
        const text = document.getElementById('percent');
        
        if (bar) bar.style.width = "100%";
        if (text) text.textContent = "100%";
        
        localStorage.setItem('analysisResult', JSON.stringify(resultData));

        setTimeout(() => {
            window.location.href = '/result';
        }, 500);

    } catch (error) {
        alert('분석 중 오류가 발생했습니다: ' + error);
        window.location.href = '/';
    }
}

function animateLoadingBarTo99() {
    const bar = document.getElementById('bar');
    const text = document.getElementById('percent');
    if (!bar || !text) return;

    let percent = 0;
    let interval = setInterval(function() {
        percent += Math.floor(Math.random() * 5 + 3);
        if (percent >= 99) {
            percent = 99;
            clearInterval(interval);
        }
        bar.style.width = percent + "%";
        text.textContent = percent + "%";
    }, 300);
}

// result.html 페이지 로드 시 실행
function displayResults() {
    const resultDataString = localStorage.getItem('analysisResult');
    if (!resultDataString) {
        document.querySelector('#results-container').innerHTML = '<div class="result-section error-box"><h3>오류</h3><p>결과 데이터를 찾을 수 없습니다. 다시 시도해 주세요.</p></div>';
        return;
    }

    const data = JSON.parse(resultDataString);
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';

    let htmlContent = '';

    if (data.error) {
        htmlContent = `<div class="result-section error-box">
                         <h3>분석 실패</h3>
                         <p>${data.error}</p>
                       </div>`;
    } else {
        htmlContent = `
        <div class="results-grid">
            <div class="result-card">
                <h3>요약 결과</h3>
                <p>${data.summary || '요약 정보 없음'}</p>
            </div>

            <div class="result-card sentiment-card">
                <h3>감정 분석</h3>
                <ul>
                    <li>긍정: ${data.sentiment.positive_count}개</li>
                    <li>부정: ${data.sentiment.negative_count}개</li>
                    <li>중립: ${data.sentiment.neutral_count}개</li>
                    <li><b>총평:</b> ${data.sentiment.overall_analysis}</li>
                </ul>
            </div>

            <div class="result-card trust-card">
                <h3>신뢰도 점수</h3>
                <p><b>${data.trust_score.score} / 100점</b></p>
                <p><b>판단 근거:</b> ${data.trust_score.reason}</p>
            </div>
        </div>

        <div class="result-section full-width">
            <h3>□ ${data.filter_info || '분석에 사용된 리뷰'}</h3>
            <ul>
                ${data.reviews.map(r => `<li>${r.substring(0, 150)}...</li>`).join('')}
            </ul>
        </div>`;
    }
    resultsContainer.innerHTML = htmlContent;
    localStorage.removeItem('analysisResult');
}