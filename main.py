import csv
import os

# Đường dẫn thư mục input và output
input_dir = 'input'
output_dir = 'output'
config_file = 'config.csv'  # File chứa scada_id và tên trạm điện mới

# Kiểm tra và tạo thư mục input nếu chưa tồn tại
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    print(f"Đã tạo thư mục: {input_dir}. Vui lòng bỏ các file .ddl vào thư mục này và chạy lại chương trình.")
    exit()

# Kiểm tra và tạo thư mục output nếu chưa tồn tại
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Đã tạo thư mục: {output_dir}")

try:
    # Đọc file config.csv để lấy các cặp scada_id và new_substation_name
    with open(config_file, mode='r') as csvfile:
        # Loại bỏ khoảng trắng xung quanh tiêu đề và dữ liệu
        reader = csv.DictReader(csvfile)
        config_data = [(row['scada id'].strip(), row['substation'].strip()) for row in reader]

    # Duyệt qua tất cả các file .ddl trong thư mục input
    for input_filename in os.listdir(input_dir):
        if input_filename.endswith('.ddl'):
            input_file_path = os.path.join(input_dir, input_filename)
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(input_filename)[0]}_done.ddl")

            # Đọc nội dung file .ddl
            with open(input_file_path, 'r') as file:
                lines = file.readlines()

            # Duyệt qua từng cặp scada_id và new_substation_name trong config.csv
            for scada_id, new_substation_name in config_data:
                # Duyệt qua tất cả các dòng trong file .ddl để tìm SCADA ID
                for i, line in enumerate(lines):
                    # Kiểm tra dòng chứa SCADA ID
                    if f'record("DEVICE") record_key("{scada_id}")' in line:
                        # Dịch chuyển lên 2 dòng để xác định dòng record("SUBSTN")
                        substation_line_index = i - 2

                        # Kiểm tra xem có đủ dòng để dịch chuyển không
                        if substation_line_index >= 0 and 'record("SUBSTN")' in lines[substation_line_index]:
                            # Giữ nguyên định dạng và thay thế tên trạm điện
                            original_line = lines[substation_line_index]
                            # Tìm vị trí record_key và thay thế tên trạm điện
                            updated_line = original_line.split('record_key("')[0] + f'record_key("{new_substation_name}")\n'
                            lines[substation_line_index] = updated_line
                        else:
                            print(f"Không tìm thấy dòng record('SUBSTN') tương ứng cho SCADA ID {scada_id} trong file {input_filename}.")

            # Ghi nội dung đã chỉnh sửa vào file .ddl mới sau khi xử lý tất cả các cặp
            with open(output_file_path, 'w') as file:
                file.writelines(lines)

            print(f"Đã xử lý file {input_filename} và xuất ra file: {output_file_path}")

except FileNotFoundError as e:
    print(f"Không tìm thấy file {str(e)} trong thư mục hiện tại.")
except KeyError as e:
    print(f"Đã xảy ra lỗi: Cột {e} không tồn tại trong file config.csv. Kiểm tra lại tên cột.")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
