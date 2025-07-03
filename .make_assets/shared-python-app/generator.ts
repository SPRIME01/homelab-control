// .make_assets/shared-python-app/generator.ts
import {
  addProjectConfiguration,
  formatFiles,
  generateFiles,
  joinPathFragments,
  Tree,
  readJson,
  updateJson,
} from "@nx/devkit";
import { applicationGenerator as pythonApplicationGenerator } from "@nxlv/python"; // Import original
import { runCommandsExecutorSchema } from "@nx/devkit/executors";

interface SharedPythonAppGeneratorSchema {
  name: string;
  directory?: string;
  tags?: string;
  projectNameAndRootFormat?: "as-provided" | "derived";
  addModuleSpecifier?: boolean;
}

export default async function (
  tree: Tree,
  options: SharedPythonAppGeneratorSchema
) {
  await pythonApplicationGenerator(tree, {
    name: options.name,
    directory: options.directory,
    tags: options.tags,
    projectNameAndRootFormat: options.projectNameAndRootFormat,
    addModuleSpecifier: options.addModuleSpecifier,
  });

  const projectName = options.name; // Nx will derive this
  const projectRoot = options.directory
    ? joinPathFragments(options.directory, options.name)
    : `apps/${options.name}`;

  const projectConfigPath = joinPathFragments(projectRoot, "project.json");
  updateJson(tree, projectConfigPath, (json) => {
    if (json.targets) {
      delete json.targets.lint;
      delete json.targets.test;

      json.targets.lint = {
        executor: "nx:run-commands",
        options: {
          command: `uv run -- ruff check ${projectRoot}`,
          cwd: ".",
        },
        inputs: ["{projectRoot}/**/*"],
        outputs: [],
      } as runCommandsExecutorSchema;

      json.targets.format = {
        executor: "nx:run-commands",
        options: {
          command: `uv run -- ruff format ${projectRoot}`,
          cwd: ".",
        },
        inputs: ["{projectRoot}/**/*"],
        outputs: [],
      } as runCommandsExecutorSchema;

      json.targets.typecheck = {
        executor: "nx:run-commands",
        options: {
          command: `uv run -- mypy ${projectRoot}`,
          cwd: ".",
        },
        inputs: ["{projectRoot}/**/*"],
        outputs: [],
      } as runCommandsExecutorSchema;

      json.targets.test = {
        executor: "nx:run-commands",
        options: {
          command: `uv run -- pytest ${projectRoot}`,
          cwd: ".",
        },
        inputs: ["{projectRoot}/**/*"],
        outputs: ["coverage/{projectName}"],
        dependsOn: ["install-deps"],
      } as runCommandsExecutorSchema;

      json.targets["install-deps"] = {
        executor: "nx:run-commands",
        options: {
          command: `uv sync`,
          cwd: projectRoot,
        },
        inputs: [`${projectRoot}/pyproject.toml`, `${projectRoot}/uv.lock`],
        outputs: [`${projectRoot}/.venv`],
      } as runCommandsExecutorSchema;

      if (json.projectType === "application") {
        json.targets.serve = {
          executor: "nx:run-commands",
          options: {
            command: `uv run -- uvicorn ${projectRoot
              .replace(/apps\//, "")
              .replace(/-/g, "_")}.main:app --reload`,
            cwd: ".",
          },
          dependsOn: ["install-deps"],
        } as runCommandsExecutorSchema;
      }
    }
    return json;
  });

  const pyprojectTomlContent = `
  [project]
  name = "${projectName.replace(/-/g, "_")}"
  version = "0.1.0"
  dependencies = [
      # Add project-specific runtime dependencies here
  ]

  [project.optional-dependencies]
  dev = [
      "pytest",
      "pytest-cov",
      # Add other dev dependencies specific to this project if needed
  ]

  [tool.ruff]
  line-length = 120
  select = ["E", "F", "I"]

  [tool.mypy]
  strict = true
  ignore_missing_imports = true
    `;
  tree.write(
    joinPathFragments(projectRoot, "pyproject.toml"),
    pyprojectTomlContent
  );

  await formatFiles(tree);
}
