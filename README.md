# DeepRMSA

Mã nguồn mô phỏng bài toán **Routing and Spectrum Assignment (RSA)** trong mạng quang đàn hồi (Elastic Optical Network), sử dụng học tăng cường sâu. Dự án gồm phần huấn luyện tác tử A3C trên topology NSFNET và chương trình benchmark các thuật toán First-Fit.

> README này mô tả cách chạy theo cấu hình hiện có trong mã nguồn. Dự án chưa kèm tệp khóa phiên bản thư viện; hãy ghi lại phiên bản Python và thư viện thực tế dùng trong lần chạy của bạn để người khác có thể tái lập kết quả.

## Nội dung

- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Yêu cầu](#yêu-cầu)
- [Cài đặt](#cài-đặt)
- [Chạy huấn luyện](#chạy-huấn-luyện)
- [Chạy benchmark](#chạy-benchmark)
- [Tham số chính](#tham-số-chính)
- [Tái lập Fig. 7](#tái-lập-fig-7)
- [Kết quả đầu ra](#kết-quả-đầu-ra)
- [Lưu ý](#lưu-ý)
- [Nguồn và ghi nhận](#nguồn-và-ghi-nhận)

## Cấu trúc dự án

| Tệp/thư mục | Mô tả |
| --- | --- |
| `Deep_RMSA_A3C.py` | Khởi tạo topology, cấu hình mô phỏng và các worker A3C; chạy huấn luyện khi được thực thi. |
| `DeepRMSA_Agent.py` | Logic mô phỏng yêu cầu kết nối, tương tác môi trường và cập nhật tác tử. |
| `AC_Net.py` | Mạng actor-critic dùng TensorFlow. |
| `K-SP-FF benchmark_NSFNET.py` | Mô phỏng benchmark SP-FF hoặc KSP-FF trên NSFNET. |
| `Src_Dst_Paths.dat` | Dữ liệu nhị phân các đường đi ứng viên, được chương trình huấn luyện và benchmark đọc. |
| `model/` | Checkpoint TensorFlow có sẵn (nếu được giữ trong repository). |
| `Average_And_Plot.py` | Công cụ phân tích/plot kết quả; hiện có đường dẫn Excel cố định trong mã nguồn và cần chỉnh sửa cho máy của bạn. |
| `*.dat` | Các tệp số liệu kết quả huấn luyện/benchmark, tùy theo lần chạy. |

## Yêu cầu

- Python 3
- NumPy
- SciPy
- TensorFlow với API `tensorflow.compat.v1`
- `tf-slim`
- Để chạy phần phân tích/plot: Matplotlib, `xlrd`, `XlsxWriter`

Phiên bản tương thích cụ thể chưa được khai báo trong repo. TensorFlow và Python có yêu cầu tương thích phiên bản riêng; nếu gặp lỗi cài đặt, hãy dùng môi trường Python/TensorFlow tương thích với TensorFlow 1 compatibility mode và cập nhật các phiên bản đã kiểm chứng tại đây.

## Cài đặt

Mở terminal tại thư mục dự án, tạo môi trường ảo và cài các thư viện:

```bash
python -m venv .venv
```

Kích hoạt môi trường trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Trên macOS/Linux:

```bash
source .venv/bin/activate
```

Cài thư viện cần cho huấn luyện và benchmark:

```bash
python -m pip install --upgrade pip
python -m pip install numpy scipy tensorflow tf-slim
```

Nếu dùng script plot:

```bash
python -m pip install matplotlib xlrd XlsxWriter
```

Đảm bảo `Src_Dst_Paths.dat` nằm cùng thư mục với các script trước khi chạy.

## Chạy huấn luyện

```bash
python Deep_RMSA_A3C.py
```

Script chạy mô phỏng huấn luyện nhiều worker trên CPU theo cấu hình mặc định trong mã. Khi bắt đầu chạy mới, `load_model` được đặt là `False`. Muốn tiếp tục từ checkpoint, đặt `load_model = True` trong `Deep_RMSA_A3C.py` và đảm bảo thư mục `model/` chứa checkpoint hợp lệ.

## Chạy benchmark

```bash
python "K-SP-FF benchmark_NSFNET.py"
```

Tham số `kpath` trong script điều khiển số đường được xét: giá trị `1` tương ứng SP-FF và `5` tương ứng KSP-FF theo chú thích trong mã. Hãy kiểm tra các tham số tải và thời gian mô phỏng ở đầu script trước khi chạy để kết quả đúng với kịch bản cần so sánh.

## Tham số chính

Các thiết lập hiện nằm trực tiếp trong `Deep_RMSA_A3C.py` và script benchmark, chưa được tách thành tệp cấu hình:

- `lambda_req`: tải yêu cầu trung bình.
- `lambda_time`: thời gian phục vụ trung bình.
- `episode_size`: số yêu cầu trong một episode.
- `batch_size`: kích thước batch cập nhật.
- `num_agents`: số worker, bị giới hạn bởi `max_cpu`.
- `nonuniform`: chọn phân phối lưu lượng không đồng đều nếu bật.
- `k_path`: số đường ứng viên dùng trong quyết định định tuyến.

## Tái lập Fig. 7

Thư mục [`reproduce_fig7/`](reproduce_fig7/README_FIG7.md) là bản sao thí nghiệm riêng, giữ nguyên source gốc và bổ sung cấu hình NSFNET theo bài báo, script vẽ Fig. 7 cùng dữ liệu benchmark SP-FF/KSP-FF. Đây là phần bổ sung quy trình tái lập và kết quả thí nghiệm, không phải một thuật toán DeepRMSA mới.

Kết quả benchmark hiện có (mỗi đường mô phỏng 5.000.000 yêu cầu):

| Thuật toán | Blocking Probability trung bình | Trạng thái |
| --- | ---: | --- |
| SP-FF | 0,1282678 | Hoàn tất |
| KSP-FF | 0,0511504 | Hoàn tất |
| DeepRMSA-FLX | 0,046 ở điểm log mới nhất | Chưa hoàn tất; log mới nhất có 270 episode (~270.000 yêu cầu) |
| DeepRMSA-EP | — | Chưa có implementation đã xác minh trong source hiện có |

DeepRMSA-FLX có số liệu giữa chừng; không nên xem điểm BP mới nhất là kết quả cuối hoặc bằng chứng hội tụ. Hướng dẫn, cấu hình, CSV và giới hạn tái lập được ghi trong [README_FIG7.md](reproduce_fig7/README_FIG7.md). Script tạo hình là [`plot_fig7.py`](reproduce_fig7/plot_fig7.py); hình xem trước và log FLX đang bị loại khỏi Git qua `.gitignore`.

## Kết quả đầu ra

Trong khi chạy, tác tử có thể tạo thư mục `train_agent_<id>/` để ghi log TensorBoard. Checkpoint được ghi vào `model/`. Các file số liệu như `BP.dat`, `rewards.dat`, `policy_loss.dat`, `value_loss.dat` và `entropy.dat` được dùng để lưu các chỉ số mô phỏng/huấn luyện tùy theo luồng chạy.

## Lưu ý

- Các script đọc `Src_Dst_Paths.dat` bằng đường dẫn tương đối; chạy lệnh từ thư mục dự án.
- Huấn luyện có thể cần thời gian và tài nguyên CPU đáng kể; số worker mặc định là 16.
- `Average_And_Plot.py` đang tham chiếu các đường dẫn Excel trên một máy Windows cụ thể. Cần sửa các đường dẫn đó và chuẩn bị đúng workbook đầu vào trước khi dùng.
- Chạy thử trên môi trường mới và ghi lại cấu hình/phiên bản thư viện trước khi công bố kết quả.

## Nguồn và ghi nhận

Trong mã nguồn có ghi tác giả gốc là **Xiaoliang Chen** và **NGNS Lab, UC Davis**. Nếu repo này được chỉnh sửa từ công trình hoặc repository khác, hãy bổ sung trích dẫn bài báo và liên kết nguồn gốc tại đây, đồng thời kiểm tra giấy phép của mã nguồn trước khi công khai. Chưa thêm giấy phép mới vì chưa xác định quyền cấp phép phù hợp.
