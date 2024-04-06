import sys, yaml, os, glob, jinja2, shutil

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} <services-folder> <output-config> <output-checkers> <checksystem-checkers-basedir>")
        print(f"Example: {sys.argv[0]} ./services ./cs.services.conf ./checkers /app/checkers")
        sys.exit(1)
    services_folder = sys.argv[1]
    output_config = sys.argv[2]
    output_checkers = sys.argv[3]
    checkers_basedir = sys.argv[4]

    # search services.yml files
    yamls = glob.iglob(os.path.join(services_folder, "**/services.yml"), recursive=True)

    # retrieve all checkers
    checker_data = []
    for config_path in yamls:
        config = yaml.load(open(config_path, 'rt', encoding='utf8'), yaml.Loader)
        for slug, service in config['services'].items():
            checker_data.append({
                "name": service["name"],
                "slug": slug,
                "path": os.path.join(os.path.dirname(config_path), service["checker"]["basedir"]),
                "script": os.path.join(checkers_basedir, slug, service["checker"]["script"]),
                "setup": service["checker"]["setup"],
            })
        print(f"Loaded {len(config['services'])} services from {config_path}")
    
    checker_template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string("""
{
  services => [
        {% for checker in checkers %}{name => '{{ checker.name }}', path => '{{ checker.script }}', timeout => 10},{% endfor %}
  ],
}
""".strip())
    
    # write cs.services.conf
    with open(output_config, 'w') as f:
        f.write(checker_template.render(checkers=checker_data))

    # copy checkers
    os.makedirs(output_checkers, exist_ok=True)
    for checker in checker_data:
        shutil.copytree(checker["path"], os.path.join(output_checkers, checker["slug"]))

    with open(os.path.join(output_checkers, "setup.sh"), "w") as f:
        f.write("#!/bin/bash\nset -e\n" + "\n".join(f"(cd {checker['slug']}; {checker['setup']})" for checker in checker_data))

    os.chmod(os.path.join(output_checkers, "setup.sh"), 0o777)
    
