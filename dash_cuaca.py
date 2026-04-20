import requests
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# =========================================================
# DATA LOKASI INDONESIA
# =========================================================
data_lokasi = {
    "Jawa Timur": {
        "Surabaya": {"lat": -7.2575, "lon": 112.7521},
        "Malang": {"lat": -7.9666, "lon": 112.6326},
        "Kediri": {"lat": -7.8167, "lon": 112.0167},
        "Blitar": {"lat": -8.0983, "lon": 112.1681},
        "Madiun": {"lat": -7.6298, "lon": 111.5239},
        "Mojokerto": {"lat": -7.4706, "lon": 112.4336},
        "Pasuruan": {"lat": -7.6453, "lon": 112.9075},
        "Probolinggo": {"lat": -7.7543, "lon": 113.2159},
        "Banyuwangi": {"lat": -8.2192, "lon": 114.3691},
        "Jember": {"lat": -8.1724, "lon": 113.7000},
        "Sidoarjo": {"lat": -7.4478, "lon": 112.7183},
        "Gresik": {"lat": -7.1568, "lon": 112.6555}
    },
    "DKI Jakarta": {
        "Jakarta Pusat": {"lat": -6.1865, "lon": 106.8341},
        "Jakarta Utara": {"lat": -6.1384, "lon": 106.8637},
        "Jakarta Barat": {"lat": -6.1683, "lon": 106.7588},
        "Jakarta Selatan": {"lat": -6.2615, "lon": 106.8106},
        "Jakarta Timur": {"lat": -6.2250, "lon": 106.9004}
    },
    "Jawa Barat": {
        "Bandung": {"lat": -6.9175, "lon": 107.6191},
        "Bekasi": {"lat": -6.2383, "lon": 106.9756},
        "Bogor": {"lat": -6.5950, "lon": 106.8166},
        "Depok": {"lat": -6.4025, "lon": 106.7942},
        "Sukabumi": {"lat": -6.9277, "lon": 106.9294},
        "Cirebon": {"lat": -6.7320, "lon": 108.5523},
        "Tasikmalaya": {"lat": -7.3274, "lon": 108.2207}
    },
    "Jawa Tengah": {
        "Semarang": {"lat": -6.9667, "lon": 110.4167},
        "Surakarta": {"lat": -7.5666, "lon": 110.8167},
        "Magelang": {"lat": -7.4706, "lon": 110.2177},
        "Salatiga": {"lat": -7.3319, "lon": 110.4928},
        "Tegal": {"lat": -6.8694, "lon": 109.1402},
        "Pekalongan": {"lat": -6.8898, "lon": 109.6744}
    },
    "DI Yogyakarta": {
        "Yogyakarta": {"lat": -7.7956, "lon": 110.3695},
        "Sleman": {"lat": -7.7167, "lon": 110.3556},
        "Bantul": {"lat": -7.8880, "lon": 110.3288},
        "Kulon Progo": {"lat": -7.8267, "lon": 110.1641},
        "Gunungkidul": {"lat": -7.9960, "lon": 110.6048}
    },
    "Bali": {
        "Denpasar": {"lat": -8.6705, "lon": 115.2126},
        "Singaraja": {"lat": -8.1120, "lon": 115.0882},
        "Ubud": {"lat": -8.5069, "lon": 115.2625},
        "Tabanan": {"lat": -8.5413, "lon": 115.1252}
    },
    "Sumatera Utara": {
        "Medan": {"lat": 3.5952, "lon": 98.6722},
        "Binjai": {"lat": 3.6001, "lon": 98.4854},
        "Pematangsiantar": {"lat": 2.9595, "lon": 99.0687}
    },
    "Sumatera Barat": {
        "Padang": {"lat": -0.9471, "lon": 100.4172},
        "Bukittinggi": {"lat": -0.3056, "lon": 100.3692},
        "Payakumbuh": {"lat": -0.2280, "lon": 100.6324}
    },
    "Riau": {
        "Pekanbaru": {"lat": 0.5333, "lon": 101.4500},
        "Dumai": {"lat": 1.6664, "lon": 101.4478}
    },
    "Kepulauan Riau": {
        "Batam": {"lat": 1.0456, "lon": 104.0305},
        "Tanjungpinang": {"lat": 0.9186, "lon": 104.4665}
    },
    "Sumatera Selatan": {
        "Palembang": {"lat": -2.9761, "lon": 104.7754},
        "Lubuklinggau": {"lat": -3.2967, "lon": 102.8617}
    },
    "Lampung": {
        "Bandar Lampung": {"lat": -5.4292, "lon": 105.2610},
        "Metro": {"lat": -5.1131, "lon": 105.3067}
    },
    "Kalimantan Timur": {
        "Samarinda": {"lat": -0.5022, "lon": 117.1537},
        "Balikpapan": {"lat": -1.2379, "lon": 116.8529},
        "Bontang": {"lat": 0.1324, "lon": 117.4854}
    },
    "Kalimantan Selatan": {
        "Banjarmasin": {"lat": -3.3186, "lon": 114.5944},
        "Banjarbaru": {"lat": -3.4420, "lon": 114.8450}
    },
    "Kalimantan Barat": {
        "Pontianak": {"lat": -0.0263, "lon": 109.3425},
        "Singkawang": {"lat": 0.9000, "lon": 108.9833}
    },
    "Sulawesi Selatan": {
        "Makassar": {"lat": -5.1477, "lon": 119.4327},
        "Parepare": {"lat": -4.0135, "lon": 119.6255},
        "Palopo": {"lat": -2.9925, "lon": 120.1969}
    },
    "Sulawesi Utara": {
        "Manado": {"lat": 1.4748, "lon": 124.8421},
        "Bitung": {"lat": 1.4451, "lon": 125.1824},
        "Tomohon": {"lat": 1.3230, "lon": 124.8389}
    },
    "Papua": {
        "Jayapura": {"lat": -2.5337, "lon": 140.7181}
    },
    "Papua Barat": {
        "Sorong": {"lat": -0.8762, "lon": 131.2558},
        "Manokwari": {"lat": -0.8615, "lon": 134.0788}
    },
    "Nusa Tenggara Barat": {
        "Mataram": {"lat": -8.5833, "lon": 116.1167},
        "Bima": {"lat": -8.4606, "lon": 118.7274}
    },
    "Nusa Tenggara Timur": {
        "Kupang": {"lat": -10.1772, "lon": 123.6070},
        "Maumere": {"lat": -8.6199, "lon": 122.2111}
    }
}

ikon_cuaca = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌧️",
    61: "🌧️", 63: "🌧️", 65: "⛈️",
    71: "🌨️", 73: "🌨️", 75: "❄️",
    80: "🌦️", 81: "🌧️", 82: "⛈️",
    95: "⛈️", 96: "⛈️", 99: "⛈️"
}

def ambil_ikon(kode_cuaca):
    return ikon_cuaca.get(kode_cuaca, "🌈")

def ambil_data_cuaca(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min"
        f"&timezone=auto&forecast_days=5"
    )
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    data = response.json()

    saat_ini = data["current"]
    harian = data["daily"]

    prakiraan = []
    for i in range(len(harian["time"])):
        prakiraan.append({
            "tanggal": harian["time"][i],
            "kode_cuaca": harian["weather_code"][i],
            "suhu_maks": harian["temperature_2m_max"][i],
            "suhu_min": harian["temperature_2m_min"][i],
        })

    return {
        "suhu": saat_ini["temperature_2m"],
        "kelembapan": saat_ini["relative_humidity_2m"],
        "angin": saat_ini["wind_speed_10m"],
        "kode_cuaca": saat_ini["weather_code"],
        "prakiraan": prakiraan
    }

def buat_peta(nama_lokasi, lat, lon, suhu):
    data_peta = pd.DataFrame({
        "Lokasi": [nama_lokasi],
        "Latitude": [lat],
        "Longitude": [lon],
        "Suhu": [suhu]
    })

    fig = px.scatter_mapbox(
        data_peta,
        lat="Latitude",
        lon="Longitude",
        hover_name="Lokasi",
        hover_data={"Suhu": True, "Latitude": False, "Longitude": False},
        zoom=6,
        height=300
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

app = Dash(__name__)
app.title = "Dashboard Cuaca Indonesia"

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: "Segoe UI", Arial, sans-serif;
                background: linear-gradient(180deg, #35527a 0%, #45688f 100%);
                overflow-x: hidden;
            }

            .kulit-aplikasi {
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
                padding: 24px;
            }

            .pembungkus-utama {
                position: relative;
                z-index: 2;
                display: grid;
                grid-template-columns: 420px minmax(520px, 1fr);
                gap: 24px;
                max-width: 1280px;
                margin: 0 auto;
                align-items: start;
            }

            .panel-kiri, .panel-kanan {
                display: flex;
                flex-direction: column;
                gap: 20px;
                min-width: 0;
            }

            .judul-utama {
                color: white;
                font-size: 64px;
                font-weight: 800;
                margin: 0;
                line-height: 1;
                text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }

            .info-kecil {
                color: rgba(255,255,255,0.88);
                font-size: 16px;
                margin: 0 0 12px 4px;
            }

            .kotak-kontrol {
                background: rgba(255,255,255,0.12);
                backdrop-filter: blur(8px);
                border-radius: 28px;
                padding: 20px;
                width: 100%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.18);
                position: relative;
                z-index: 999;
                overflow: visible !important;
            }

            .teks-label {
                display: block;
                color: white;
                font-weight: 700;
                margin-bottom: 10px;
                font-size: 16px;
            }

            .jarak-bawah {
                margin-bottom: 16px;
            }

            .kartu-cuaca {
                background: linear-gradient(180deg, #36539a 0%, #5e79aa 45%, #f1a057 100%);
                border-radius: 34px;
                box-shadow: 0 18px 40px rgba(0,0,0,0.25);
                color: white;
                position: relative;
                overflow: hidden;
                width: 100%;
                z-index: 1;
            }

            .kartu-utama {
                padding: 28px 24px;
                min-height: 520px;
                text-align: center;
            }

            .kartu-prakiraan,
            .kartu-peta {
                padding: 22px;
            }

            .ikon-utama {
                font-size: 90px;
                margin-top: 4px;
                margin-bottom: 10px;
                line-height: 1;
            }

            .nama-kota {
                font-size: 26px;
                font-weight: 800;
                line-height: 1.25;
                margin-top: 12px;
                word-break: break-word;
            }

            .nama-hari {
                margin-top: 18px;
                font-size: 22px;
                font-weight: 700;
            }

            .nama-tanggal {
                font-size: 18px;
                font-weight: 600;
                opacity: 0.95;
                margin-bottom: 20px;
            }

            .label-suhu {
                font-size: 20px;
                opacity: 0.95;
            }

            .suhu-utama {
                font-size: 54px;
                font-weight: 800;
                margin-top: 8px;
                margin-bottom: 18px;
                line-height: 1;
            }

            .info-tambahan {
                font-size: 17px;
                line-height: 1.9;
                background: rgba(255,255,255,0.12);
                border-radius: 18px;
                padding: 14px 16px;
                backdrop-filter: blur(4px);
                text-align: left;
            }

            .judul-bagian {
                font-size: 24px;
                font-weight: 800;
                margin-bottom: 18px;
            }

            .daftar-prakiraan {
                display: grid;
                grid-template-columns: repeat(5, minmax(88px, 1fr));
                gap: 14px;
            }

            .item-prakiraan {
                min-height: 148px;
                background: rgba(255,255,255,0.12);
                border-radius: 22px;
                text-align: center;
                padding: 12px 8px;
                backdrop-filter: blur(4px);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }

            .hari-prakiraan {
                font-size: 15px;
                font-weight: 700;
                margin-bottom: 10px;
            }

            .ikon-prakiraan {
                font-size: 30px;
                margin-bottom: 10px;
                line-height: 1;
            }

            .suhu-prakiraan {
                font-size: 15px;
                font-weight: 700;
                line-height: 1.35;
            }

            .kartu-peta .js-plotly-plot,
            .kartu-peta .plot-container {
                border-radius: 22px !important;
                overflow: hidden !important;
            }

            /* FIX DROPDOWN SUPAYA MEMANJANG KE DEPAN */
            .kotak-kontrol .Select,
            .kotak-kontrol .Select-control,
            .kotak-kontrol .Select-menu-outer,
            .kotak-kontrol .Select-menu,
            .kotak-kontrol .VirtualizedSelectOption,
            .kotak-kontrol .VirtualizedSelectFocusedOption {
                z-index: 9999 !important;
            }

            .kotak-kontrol .Select-menu-outer {
                max-height: 320px !important;
                overflow-y: auto !important;
                position: absolute !important;
                width: 100% !important;
                left: 0 !important;
                top: calc(100% + 4px) !important;
                border-radius: 12px !important;
            }

            .kotak-kontrol .Select.is-open {
                z-index: 10000 !important;
            }

            .kotak-kontrol .Select-control {
                overflow: visible !important;
            }

            .meteor {
                position: absolute;
                top: -120px;
                width: 3px;
                height: 120px;
                background: linear-gradient(to bottom, rgba(255,255,255,0.95), rgba(255,255,255,0));
                transform: rotate(35deg);
                opacity: 0.8;
                z-index: 1;
                border-radius: 999px;
                box-shadow: 0 0 16px rgba(255,255,255,0.5);
                animation: meteorJatuh linear infinite;
                pointer-events: none;
            }

            .meteor::before {
                content: "";
                position: absolute;
                top: -10px;
                left: -4px;
                width: 12px;
                height: 12px;
                background: white;
                border-radius: 50%;
                box-shadow: 0 0 14px rgba(255,255,255,0.95);
            }

            .meteor-1 { left: 15%; animation-duration: 8s; animation-delay: 0s; }
            .meteor-2 { left: 55%; animation-duration: 10s; animation-delay: 2s; }
            .meteor-3 { left: 85%; animation-duration: 9s; animation-delay: 4s; }

            @keyframes meteorJatuh {
                0% {
                    transform: translate(0, 0) rotate(35deg);
                    opacity: 0;
                }
                8% {
                    opacity: 1;
                }
                100% {
                    transform: translate(220px, 650px) rotate(35deg);
                    opacity: 0;
                }
            }

            @media (max-width: 1100px) {
                .pembungkus-utama {
                    grid-template-columns: 1fr;
                }

                .judul-utama {
                    font-size: 52px;
                }

                .daftar-prakiraan {
                    grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
                }
            }

            @media (max-width: 640px) {
                .kulit-aplikasi {
                    padding: 16px;
                }

                .judul-utama {
                    font-size: 44px;
                }

                .info-kecil {
                    font-size: 14px;
                }

                .nama-kota {
                    font-size: 22px;
                }

                .suhu-utama {
                    font-size: 46px;
                }

                .daftar-prakiraan {
                    grid-template-columns: repeat(2, minmax(90px, 1fr));
                }

                .item-prakiraan {
                    min-height: 132px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

provinsi_awal = "Jawa Timur"

app.layout = html.Div(
    className="kulit-aplikasi",
    children=[
        html.Div(className="meteor meteor-1"),
        html.Div(className="meteor meteor-2"),
        html.Div(className="meteor meteor-3"),

        html.Div(
            className="pembungkus-utama",
            children=[
                html.Div(
                    className="panel-kiri",
                    children=[
                        html.H1("Cuaca", className="judul-utama"),
                        html.P("38 Provinsi • Berbagai Kota dan Daerah di Indonesia", className="info-kecil"),

                        html.Div(
                            className="kotak-kontrol",
                            children=[
                                html.Label("Pilih Provinsi", className="teks-label"),
                                html.Div(
                                    dcc.Dropdown(
                                        id="dropdown-provinsi",
                                        options=[{"label": p, "value": p} for p in data_lokasi.keys()],
                                        value=provinsi_awal,
                                        clearable=False,
                                        searchable=True,
                                        optionHeight=40,
                                        maxHeight=320
                                    ),
                                    className="jarak-bawah"
                                ),

                                html.Label("Pilih Kota / Daerah", className="teks-label"),
                                dcc.Dropdown(
                                    id="dropdown-kota",
                                    clearable=False,
                                    searchable=True,
                                    optionHeight=40,
                                    maxHeight=320
                                ),
                            ]
                        ),

                        html.Div(
                            className="kartu-cuaca kartu-utama",
                            children=[
                                html.Div(id="ikon-utama", className="ikon-utama"),
                                html.Div(id="nama-kota", className="nama-kota"),
                                html.Div(id="nama-hari", className="nama-hari"),
                                html.Div(id="nama-tanggal", className="nama-tanggal"),
                                html.Div("Suhu", className="label-suhu"),
                                html.Div(id="suhu-utama", className="suhu-utama"),
                                html.Div(id="info-tambahan", className="info-tambahan"),
                            ]
                        ),
                    ]
                ),

                html.Div(
                    className="panel-kanan",
                    children=[
                        html.Div(
                            className="kartu-cuaca kartu-prakiraan",
                            children=[
                                html.Div("Prakiraan 5 Hari", className="judul-bagian"),
                                html.Div(id="daftar-prakiraan", className="daftar-prakiraan"),
                            ]
                        ),

                        html.Div(
                            className="kartu-cuaca kartu-peta",
                            children=[
                                html.Div("Peta Lokasi", className="judul-bagian"),
                                dcc.Graph(id="grafik-peta", config={"displayModeBar": False})
                            ]
                        )
                    ]
                ),

                dcc.Interval(id="interval-pembaruan", interval=60 * 1000, n_intervals=0),
            ]
        )
    ]
)

@app.callback(
    Output("dropdown-kota", "options"),
    Output("dropdown-kota", "value"),
    Input("dropdown-provinsi", "value")
)
def perbarui_dropdown_kota(provinsi_terpilih):
    opsi_kota = [
        {"label": kota, "value": kota}
        for kota in data_lokasi[provinsi_terpilih].keys()
    ]
    kota_pertama = list(data_lokasi[provinsi_terpilih].keys())[0]
    return opsi_kota, kota_pertama

@app.callback(
    Output("ikon-utama", "children"),
    Output("nama-kota", "children"),
    Output("nama-hari", "children"),
    Output("nama-tanggal", "children"),
    Output("suhu-utama", "children"),
    Output("info-tambahan", "children"),
    Output("daftar-prakiraan", "children"),
    Output("grafik-peta", "figure"),
    Input("dropdown-provinsi", "value"),
    Input("dropdown-kota", "value"),
    Input("interval-pembaruan", "n_intervals")
)
def perbarui_dashboard(provinsi_terpilih, kota_terpilih, _):
    if not kota_terpilih:
        kota_terpilih = list(data_lokasi[provinsi_terpilih].keys())[0]

    koordinat = data_lokasi[provinsi_terpilih][kota_terpilih]
    lat = koordinat["lat"]
    lon = koordinat["lon"]

    cuaca = ambil_data_cuaca(lat, lon)

    ikon_saat_ini = ambil_ikon(cuaca["kode_cuaca"])
    suhu_saat_ini = f"{cuaca['suhu']}°C"

    info_tambahan = html.Div([
        html.Div(f"Kelembapan Udara: {cuaca['kelembapan']}%"),
        html.Div(f"Kecepatan Angin: {cuaca['angin']} km/jam"),
    ])

    daftar_item_prakiraan = []
    nama_hari_singkat = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

    for item in cuaca["prakiraan"]:
        tanggal_obj = pd.to_datetime(item["tanggal"])
        hari = nama_hari_singkat[tanggal_obj.dayofweek]
        ikon = ambil_ikon(item["kode_cuaca"])

        daftar_item_prakiraan.append(
            html.Div(
                className="item-prakiraan",
                children=[
                    html.Div(hari, className="hari-prakiraan"),
                    html.Div(ikon, className="ikon-prakiraan"),
                    html.Div(f"{item['suhu_maks']}° / {item['suhu_min']}°", className="suhu-prakiraan"),
                ]
            )
        )

    fig = buat_peta(f"{kota_terpilih}, {provinsi_terpilih}", lat, lon, cuaca["suhu"])

    sekarang = pd.Timestamp.now()

    nama_hari_indonesia = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }

    nama_bulan_indonesia = {
        "Jan": "Jan",
        "Feb": "Feb",
        "Mar": "Mar",
        "Apr": "Apr",
        "May": "Mei",
        "Jun": "Jun",
        "Jul": "Jul",
        "Aug": "Agu",
        "Sep": "Sep",
        "Oct": "Okt",
        "Nov": "Nov",
        "Dec": "Des"
    }

    hari_sekarang = nama_hari_indonesia[sekarang.strftime("%A")]
    bulan_inggris = sekarang.strftime("%b")
    bulan_indonesia = nama_bulan_indonesia[bulan_inggris]
    tanggal_sekarang = f"{sekarang.strftime('%d')} {bulan_indonesia} {sekarang.strftime('%Y')}"

    return (
        ikon_saat_ini,
        f"{kota_terpilih.upper()}, {provinsi_terpilih.upper()}",
        hari_sekarang.upper(),
        tanggal_sekarang.upper(),
        suhu_saat_ini,
        info_tambahan,
        daftar_item_prakiraan,
        fig
    )

if __name__ == "__main__":
    app.run(debug=True)