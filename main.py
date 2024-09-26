import csv
import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import time

# Hàm xử lý chính
def run_program():
    try:
        input_dir = 'input'
        output_dir = 'output'
        config_file = 'config.csv'
        
        # Kiểm tra và tạo thư mục input nếu chưa tồn tại
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
            log_message(f"Đã tạo thư mục: {input_dir}. Vui lòng bỏ các file .ddl vào thư mục này và chạy lại chương trình.")
            return

        # Kiểm tra và tạo thư mục output nếu chưa tồn tại
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            log_message(f"Đã tạo thư mục: {output_dir}")

        # Lấy danh sách các file .ddl trong thư mục input
        ddl_files = [f for f in os.listdir(input_dir) if f.endswith('.ddl')]
        
        # Nếu không có file .ddl nào trong thư mục input, hiển thị thông báo và dừng chương trình
        if not ddl_files:
            messagebox.showwarning("Thông báo", "Vui lòng bỏ file .ddl vào thư mục input và mở lại chương trình.")
            log_message("Không tìm thấy file .ddl trong thư mục input.")
            return
        else:
            # Xóa dòng trạng thái nếu người dùng chạy lại chương trình và có file .ddl trong input
            status_label.config(text="")  # Xóa thông báo cũ

        # Đọc file config.csv để lấy các cặp scada_id và new_substation_name
        with open(config_file, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            config_data = [(row['scada id'].strip(), row['substation'].strip()) for row in reader]

        files_processed = []
        total_files = len(ddl_files)
        progress_bar["maximum"] = total_files
        processed_files_count = 0

        # Duyệt qua tất cả các file .ddl trong thư mục input
        for input_filename in ddl_files:
            input_file_path = os.path.join(input_dir, input_filename)
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(input_filename)[0]}_done.ddl")

            # Đọc nội dung file .ddl
            with open(input_file_path, 'r') as file:
                lines = file.readlines()

            # Duyệt qua từng cặp scada_id và new_substation_name trong config.csv
            for scada_id, new_substation_name in config_data:
                # Hiển thị tiến trình
                progress_label.config(text=f"Đang xử lý file {input_filename}, SCADA ID: {scada_id}")
                root.update_idletasks()

                # Duyệt qua tất cả các dòng trong file .ddl để tìm SCADA ID
                for i, line in enumerate(lines):
                    if f'record("DEVICE") record_key("{scada_id}")' in line:
                        substation_line_index = i - 2

                        if substation_line_index >= 0 and 'record("SUBSTN")' in lines[substation_line_index]:
                            original_line = lines[substation_line_index]
                            updated_line = original_line.split('record_key("')[0] + f'record_key("{new_substation_name}")\n'
                            lines[substation_line_index] = updated_line

            # Ghi nội dung đã chỉnh sửa vào file .ddl mới
            with open(output_file_path, 'w') as file:
                file.writelines(lines)

            files_processed.append(input_filename)
            processed_files_count += 1
            smooth_progress_bar(processed_files_count)

        log_message("Đã xử lý xong tất cả các file.")

        # Hiển thị hộp thoại thông báo hoàn thành
        messagebox.showinfo("Thông báo", f"Đã xử lý xong các file: {', '.join(files_processed)}")

    except FileNotFoundError as e:
        log_message(f"Không tìm thấy file {str(e)}.")
    except KeyError as e:
        log_message(f"Đã xảy ra lỗi: Cột {e} không tồn tại trong file config.csv.")
    except Exception as e:
        log_message(f"Đã xảy ra lỗi: {e}")

# Hàm để cập nhật thanh progress bar mượt mà
def smooth_progress_bar(value):
    current_value = progress_bar["value"]
    step = (value - current_value) / 20  # Tăng dần giá trị mỗi lần cập nhật
    for i in range(20):
        current_value += step
        progress_bar["value"] = current_value
        root.update_idletasks()
        time.sleep(0.02)  # Giảm tốc độ để tạo hiệu ứng mượt mà

# Hàm để ghi trạng thái vào giao diện
def log_message(message):
    status_label.config(text=message)
    root.update_idletasks()

# Tạo giao diện GUI với tkinter
root = tk.Tk()
root.title("tool doi ten tram PDS2")
root.geometry("400x400")

# Logo của chương trình
root.iconbitmap("tool.ico")

# Nút "Run"
run_button = tk.Button(root, text="Run", command=run_program, font=("Arial", 12), bg='green', fg='white')
run_button.pack(pady=10)

# Thanh trạng thái "Loading"
progress_label = tk.Label(root, text="Chương trình đang sẵn sàng.", font=("Arial", 10))
progress_label.pack(pady=5)

# Thanh loading
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

# Vùng hiển thị trạng thái
status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=5)

# Thông tin bản quyền
copyright_label = tk.Label(root, text="Copyright@ Thinhlh", font=("Arial", 8))
copyright_label.pack(side="bottom", pady=5)

# Bắt đầu vòng lặp GUI
root.mainloop()
