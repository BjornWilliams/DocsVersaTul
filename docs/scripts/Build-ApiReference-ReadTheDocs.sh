#!/usr/bin/env bash
set -euo pipefail

task_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
task_repository_root="$(cd -- "${task_script_dir}/../.." && pwd)"
task_dotnet_install_root="${HOME}/.dotnet"
task_dotnet_sdk_version="10.0.403"
task_dotnet_install_script="${TMPDIR:-/tmp}/dotnet-install-${task_dotnet_sdk_version}.sh"

cd "${task_repository_root}"

if [[ ! -x "${task_dotnet_install_root}/dotnet" ]] || [[ "$("${task_dotnet_install_root}/dotnet" --version)" != "${task_dotnet_sdk_version}" ]]; then
  curl --fail --silent --show-error --location https://dot.net/v1/dotnet-install.sh --output "${task_dotnet_install_script}"
  bash "${task_dotnet_install_script}" --version "${task_dotnet_sdk_version}" --install-dir "${task_dotnet_install_root}" --no-path
fi

export DOTNET_ROOT="${task_dotnet_install_root}"
export PATH="${DOTNET_ROOT}:${PATH}"

dotnet tool restore
python docs/scripts/build_api_reference.py
python docs/scripts/build_historical_api_reference.py
