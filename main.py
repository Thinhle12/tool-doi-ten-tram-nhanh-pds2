import csv

# Đường dẫn file đầu vào và đầu ra
input_file = 'input.ddl'
output_file = 'output.ddl'
config_file = 'config.csv'  # File chứa scada_id và tên trạm điện mới

try:
    # Đọc nội dung file .ddl một lần duy nhất
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Đọc file config.csv để lấy các cặp scada_id và new_substation_name
    with open(config_file, mode='r') as csvfile:
        # Loại bỏ khoảng trắng xung quanh tiêu đề và dữ liệu
        reader = csv.DictReader(csvfile)
        
        # Duyệt qua từng cặp scada_id và new_substation_name trong file config
        for row in reader:
            scada_id = row['scada_id'].strip()  # Loại bỏ khoảng trắng thừa nếu có
            new_substation_name = row['substation'].strip()  # Loại bỏ khoảng trắng thừa nếu có
            
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
                        print(f"Không tìm thấy dòng record('SUBSTN') tương ứng cho SCADA ID {scada_id}.")

    # Ghi nội dung đã chỉnh sửa vào file .ddl mới sau khi xử lý tất cả các cặp
    with open(output_file, 'w') as file:
        file.writelines(lines)

    print(f"Đã thay thế tên trạm điện cho tất cả các SCADA ID thành công và xuất ra file: {output_file}")

except FileNotFoundError:
    print(f"Không tìm thấy file {input_file} hoặc {config_file} trong thư mục hiện tại.")
except KeyError as e:
    print(f"Đã xảy ra lỗi: Cột {e} không tồn tại trong file config.csv. Kiểm tra lại tên cột.")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
