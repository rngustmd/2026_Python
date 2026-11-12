// ===== 서버 주소 =====
const API_URL = "http://127.0.0.1:8000/api/predict";

// ===== 화면 요소 =====
const form = document.querySelector("#predictForm");
const areaInput = document.querySelector("#area");
const submitBtn = document.querySelector("#submitBtn");
let contractYear = 2026; // 계약연도 (버튼 선택값)
const history = [];      // 최근 예측 기록

// ===== 동별 실제 데이터 범위 ( apt_data.csv 기준 ) =====
// [ 최저층, 최고층, 최초 건축년도, 최근 건축년도, 최소면적, 최대면적 ]
const RANGE = {"당산동": [1, 19, 1995, 2015, 13.3, 117.4], "당산동1가": [2, 23, 1996, 2008, 59.4, 162.2], "당산동2가": [1, 25, 1994, 1999, 31.7, 82.8], "당산동3가": [1, 23, 1979, 2014, 16.5, 134.8], "당산동4가": [1, 26, 1983, 2017, 51.5, 157.9], "당산동5가": [1, 28, 1984, 2020, 28.9, 161.1], "당산동6가": [6, 7, 2012, 2012, 13.4, 13.7], "대림동": [1, 30, 1981, 2022, 13.6, 140.5], "도림동": [1, 31, 1997, 2014, 37.6, 143.6], "문래동2가": [1, 15, 1983, 1983, 47.3, 72.9], "문래동3가": [1, 25, 1983, 2015, 57.4, 165.2], "문래동4가": [1, 21, 2001, 2008, 59.9, 85.0], "문래동5가": [1, 20, 1988, 2017, 60.0, 96.4], "문래동6가": [1, 20, 1985, 2020, 40.0, 124.4], "신길동": [1, 30, 1972, 2024, 10.8, 136.7], "양평동1가": [1, 24, 1982, 2021, 24.9, 85.0], "양평동2가": [1, 22, 1990, 1999, 40.4, 114.6], "양평동3가": [1, 25, 1990, 2018, 37.8, 131.3], "양평동4가": [1, 19, 1984, 2006, 27.0, 112.8], "양평동5가": [1, 20, 1996, 1998, 59.4, 132.2], "양평동6가": [1, 18, 1999, 2015, 43.0, 114.6], "여의도동": [1, 49, 1971, 2023, 33.7, 244.9], "영등포동": [1, 23, 1969, 2021, 30.1, 114.1], "영등포동1가": [2, 23, 2006, 2022, 12.0, 84.9], "영등포동2가": [5, 29, 2016, 2024, 14.0, 61.5], "영등포동3가": [4, 12, 2014, 2014, 13.5, 13.5], "영등포동4가": [8, 11, 2012, 2012, 12.1, 12.1], "영등포동5가": [3, 16, 1971, 1999, 60.0, 84.1], "영등포동7가": [1, 35, 1998, 2020, 17.0, 115.6], "영등포동8가": [1, 24, 1999, 2012, 12.1, 163.7]};

const dongSelect = document.querySelector("#dong");
const floorInput = document.querySelector("#floor");
const buildInput = document.querySelector("#build_year");

// 동별 실제 건축년도 목록 ( apt_data.csv 기준 )
const BUILD_YEARS = {"당산동": [1995, 2002, 2003, 2004, 2005, 2007, 2012, 2013, 2015], "당산동1가": [1996, 1997, 2008], "당산동2가": [1994, 1999], "당산동3가": [1979, 1986, 2003, 2009, 2010, 2014], "당산동4가": [1983, 1986, 1988, 1997, 1999, 2000, 2002, 2010, 2013, 2015, 2017], "당산동5가": [1984, 1997, 1999, 2001, 2002, 2003, 2005, 2020], "당산동6가": [2012], "대림동": [1981, 1985, 1987, 1989, 1992, 1995, 1997, 1998, 1999, 2001, 2005, 2007, 2008, 2011, 2012, 2013, 2016, 2018, 2020, 2022], "도림동": [1997, 1998, 2000, 2001, 2014], "문래동2가": [1983], "문래동3가": [1983, 1988, 1998, 1999, 2001, 2003, 2004, 2005, 2006, 2015], "문래동4가": [2001, 2008], "문래동5가": [1988, 1991, 1992, 2000, 2017], "문래동6가": [1985, 1986, 1987, 1991, 1996, 1997, 1998, 2020], "신길동": [1972, 1974, 1976, 1981, 1983, 1984, 1985, 1986, 1987, 1989, 1991, 1993, 1997, 1999, 2000, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2011, 2012, 2013, 2014, 2015, 2017, 2019, 2020, 2021, 2022, 2024], "양평동1가": [1982, 1994, 1996, 2005, 2006, 2019, 2021], "양평동2가": [1990, 1996, 1998, 1999], "양평동3가": [1990, 1991, 1998, 1999, 2000, 2004, 2005, 2008, 2009, 2012, 2018], "양평동4가": [1984, 1993, 2000, 2003, 2006], "양평동5가": [1996, 1998], "양평동6가": [1999, 2000, 2014, 2015], "여의도동": [1971, 1974, 1975, 1976, 1977, 1978, 1994, 2000, 2002, 2003, 2005, 2008, 2023], "영등포동": [1969, 2002, 2003, 2004, 2021], "영등포동1가": [2006, 2011, 2012, 2013, 2020, 2022], "영등포동2가": [2016, 2017, 2022, 2024], "영등포동3가": [2014], "영등포동4가": [2012], "영등포동5가": [1971, 1999], "영등포동7가": [1998, 2003, 2004, 2010, 2012, 2017, 2018, 2020], "영등포동8가": [1999, 2004, 2012]};

// 동 선택 시 건축년도 select 옵션 다시 채우기 ( 가장 가까운 연도 유지 )
function fillBuildYears() {
  const list = BUILD_YEARS[ dongSelect.value ];
  const prev = Number( buildInput.value ) || 2005;
  let best = list[0];
  list.forEach( y => { if ( Math.abs( y - prev ) < Math.abs( best - prev ) ) best = y; } );
  buildInput.innerHTML = list.map( y => `<option ${ y === best ? "selected" : "" }>${ y }</option>` ).join( "" );
}
dongSelect.addEventListener( "change", fillBuildYears );
fillBuildYears();

// 한 항목 범위 검사 : 범위 안내 문구 + 벗어나면 빨간색 표시 , 벗어났으면 true 반환
function checkOne( input, hintId, min, max, unit, label ) {
  const v = Number( input.value );
  const out = input.value !== "" && ( v < min || v > max );
  const hint = document.querySelector( "#" + hintId );
  const text = min === max ? `${ min }${ unit }` : `${ min }~${ max }${ unit }`; // 범위가 한 값이면 하나만 표시
  hint.textContent = ( out ? "⚠ 범위 밖 · " : "" ) + `${ label } 데이터 범위 ${ text }`;
  hint.classList.toggle( "out", out );
  input.classList.toggle( "out", out );
  return out;
}

// 선택한 동 기준으로 전체 검사 , 범위 밖 항목 이름 목록 반환
function checkRange() {
  const r = RANGE[ dongSelect.value ];
  const outs = [];
  if ( checkOne( areaInput, "areaRange", r[4], r[5], "㎡", "이 동" ) ) outs.push( "면적" );
  return outs;
}
dongSelect.addEventListener( "change", checkRange );

// 동 선택 시 층 select 옵션 채우기 ( 이 동의 실제 최저층 ~ 최고층 , 이전 값 유지 )
function fillFloors() {
  const r = RANGE[ dongSelect.value ];
  const prev = Number( floorInput.value ) || 10;
  const pick = Math.min( Math.max( prev, r[0] ), r[1] );
  let html = "";
  for ( let f = r[0]; f <= r[1]; f++ ) {
    html += `<option value="${ f }" ${ f === pick ? "selected" : "" }>${ f }층</option>`;
  }
  floorInput.innerHTML = html;
  document.querySelector("#floorRange").textContent = `이 동 데이터 범위 ${ r[0] }~${ r[1] }층`;
}
dongSelect.addEventListener( "change", fillFloors );
fillFloors();
areaInput.addEventListener( "input", checkRange );

// ===== 숫자 변환 함수 =====
// 만원 → "22억 5,721만원"
function toKorean( man ) {
  const eok = Math.floor( man / 10000 );
  const rest = man % 10000;
  if ( eok === 0 ) return rest.toLocaleString() + "만원";
  if ( rest === 0 ) return eok + "억원";
  return eok + "억 " + rest.toLocaleString() + "만원";
}
// ㎡ → 평
function toPyeong( m2 ) {
  return ( m2 / 3.3058 ).toFixed( 1 );
}

// ===== 면적 입력 시 평수 표시 =====
function updatePyeong() {
  const v = Number( areaInput.value );
  document.querySelector("#pyeongHint").textContent = v > 0 ? `약 ${ toPyeong( v ) }평` : "";
  document.querySelectorAll(".chip").forEach( c => {
    c.classList.toggle( "active", Number( c.dataset.area ) === v );
  } );
}
areaInput.addEventListener( "input", updatePyeong );

// 면적 빠른 선택 버튼
document.querySelectorAll(".chip").forEach( chip => {
  chip.addEventListener( "click", () => {
    areaInput.value = chip.dataset.area;
    updatePyeong();
    checkRange();
  } );
} );

// 계약연도 버튼
document.querySelectorAll("#yearSegment button").forEach( btn => {
  btn.addEventListener( "click", () => {
    document.querySelectorAll("#yearSegment button").forEach( b => b.classList.remove("active") );
    btn.classList.add("active");
    contractYear = Number( btn.dataset.year );
  } );
} );

// ===== 예측 요청 =====
form.addEventListener( "submit", async ( e ) => {
  e.preventDefault();

  // 1. 입력값을 요청 body 객체로 구성 ( 키 이름은 서버/모델 컬럼명과 동일 )
  const data = {
    dong: document.querySelector("#dong").value,
    area: Number( areaInput.value ),
    floor: Number( document.querySelector("#floor").value ),
    build_year: Number( document.querySelector("#build_year").value ),
    contract_year: contractYear
  };

  submitBtn.disabled = true;
  submitBtn.textContent = "예측 중...";
  document.querySelector("#errorMsg").classList.add("hidden");

  try {
    // 2. axios 비동기 POST 요청
    const response = await axios.post( API_URL, data );
    // 3. 응답 렌더링
    render( data, response.data );
  } catch ( err ) {
    const msg = document.querySelector("#errorMsg");
    msg.textContent = "서버 연결 실패 : AppStart.py 가 실행 중인지 확인하세요.";
    msg.classList.remove("hidden");
    console.log( err );
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "예측하기";
  }
} );

// ===== 결과 화면 그리기 =====
function render( data, res ) {
  document.querySelector("#emptyState").classList.add("hidden");
  document.querySelector("#resultBox").classList.remove("hidden");

  // 데이터 범위 밖 입력 경고 ( 예측은 하되 정확도 낮을 수 있음 안내 )
  const outs = checkRange();
  const warn = document.querySelector("#warnMsg");
  if ( outs.length > 0 ) {
    warn.textContent = `⚠ ${ data.dong }의 실제 거래 데이터에 없는 ${ outs.join(", ") } 조건이에요. 학습 범위 밖이라 예측이 부정확할 수 있어요.`;
    warn.classList.remove("hidden");
  } else {
    warn.classList.add("hidden");
  }

  // 예측 가격
  document.querySelector("#summary").textContent =
    `${ data.dong } · ${ data.area }㎡(${ toPyeong( data.area ) }평) · ${ data.floor }층 · ${ data.build_year }년식 · ${ data.contract_year }년 계약`;
  document.querySelector("#price").textContent = toKorean( res.predict );
  document.querySelector("#priceSub").textContent = `예상 거래금액 ${ res.predict.toLocaleString() }만원`;

  // 단위 가격
  document.querySelector("#perM2").textContent = Math.round( res.predict / data.area ).toLocaleString() + "만원";
  document.querySelector("#perPyeong").textContent = Math.round( res.predict / ( data.area / 3.3058 ) ).toLocaleString() + "만원";

  // 모델 성능 R²
  const percent = ( res.r2 * 100 ).toFixed( 1 );
  document.querySelector("#r2Text").textContent = res.r2.toFixed( 3 );
  document.querySelector("#r2Desc").textContent = `실제 거래가 변동의 약 ${ percent }%를 설명합니다.`;
  document.querySelector("#cvR2").textContent = res.cv_r2;
  document.querySelector("#params").textContent =
    `degree=${ res.best_params.poly__degree }, alpha=${ res.best_params.ridge__alpha }`;
  const gauge = document.querySelector("#gauge");
  gauge.style.setProperty( "--p", 0 );
  setTimeout( () => gauge.style.setProperty( "--p", percent ), 30 );

  // 최근 예측 기록 ( 최대 5개 )
  history.unshift( { text: `${ data.dong } ${ data.area }㎡ ${ data.floor }층`, price: toKorean( res.predict ) } );
  if ( history.length > 5 ) history.pop();
  document.querySelector("#historyBox").classList.remove("hidden");
  document.querySelector("#historyList").innerHTML = history
    .map( h => `<li><span>${ h.text }</span><b>${ h.price }</b></li>` )
    .join( "" );
}

updatePyeong();
checkRange();
