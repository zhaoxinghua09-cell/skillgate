# SkillGate CLI Autocompletion

## Bash

Add to ~/.bashrc:

```bash
_prog_complete() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="scan --format --output --fail-under --badge --batch --help"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _prog_complete skillgate
```

## Zsh

Add to ~/.zshrc:

```zsh
#compdef skillgate

_arguments '1:command:(scan)' \
           '--format:[Output format]:(terminal json markdown agent sarif junit)' \
           '--output:[Output file path]' \
           '--fail-under:[Minimum trust score]' \
           '--badge:[Generate badge SVG]' \
           '--batch:[Batch scan mode]' \
           '--help:[Show help]'
```

## Fish

Add to ~/.config/fish/completions/skillgate.fish:

```fish
complete -c skillgate -n "__fish_use_subcommand" -a scan
complete -c skillgate -n "__fish_seen_subcommand_from scan" -l format -d "Output format" -a "terminal json markdown agent sarif junit"
complete -c skillgate -n "__fish_seen_subcommand_from scan" -l output -d "Output file"
complete -c skillgate -n "__fish_seen_subcommand_from scan" -l fail-under -d "Minimum score to pass"
complete -c skillgate -n "__fish_seen_subcommand_from scan" -l badge -d "Generate badge SVG"
complete -c skillgate -n "__fish_seen_subcommand_from scan" -l batch -d "Batch scan mode"
```
