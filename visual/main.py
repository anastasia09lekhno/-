import os
import csv
import subprocess
import git


def read_config(config_file):
    config = {}
    with open(config_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                print(f"Ошибка в строке конфигурации: {row}")
                continue
            # Удаляем лишние символы ";" в начале строки
            config[row[0]] = row[1].lstrip(";")
    print(f"Считанная конфигурация: {config}")
    return config['path_to_plantuml'], config['repo_path'], config['output_path']


def get_commits(repo_path):
    repo = git.Repo(repo_path)
    branch_name = repo.active_branch.name  # Получаем имя активной ветки
    commits = list(repo.iter_commits(branch_name))
    return commits


def generate_plantuml(commits):
    plantuml_lines = ["@startuml"]
    for commit in commits:
        for parent in commit.parents:
            plantuml_lines.append(f"{parent.hexsha} -> {commit.hexsha}")
    plantuml_lines.append("@enduml")
    return "\n".join(plantuml_lines)

def save_plantuml_to_file(plantuml_content, file_path):
    with open(file_path, 'w') as f:
        f.write(plantuml_content)

def visualize_graph(visualizer_path, plantuml_file, output_image_path):
    # Подготовим команду для запуска PlantUML с использованием Java
    result = subprocess.run(
        ["java", "-jar", visualizer_path, plantuml_file, "-o", output_image_path],
        capture_output=True, text=True
    )

    # Проверка на ошибки выполнения
    if result.returncode == 0:
        print(f"Граф зависимостей успешно сохранён в {output_image_path}")
    else:
        print(f"Ошибка при выполнении PlantUML: {result.stderr}")

def main(config_file):
    visualizer_path, repository_path, output_image_path = read_config(config_file)
    commits = get_commits(repository_path)
    plantuml_content = generate_plantuml(commits)
    plantuml_file = "output.txt"
    save_plantuml_to_file(plantuml_content, plantuml_file)
    visualize_graph(visualizer_path, plantuml_file, output_image_path)

if __name__ == "__main__":
    config_file = "config.csv"  # Укажите путь к вашему конфигурационному файлу
    main(config_file)
