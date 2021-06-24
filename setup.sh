mkdir -p ~/.streamlit/

echo "\
[general]
email = \"sunil.kumar.sharma@mg.thedataincubator.com\"
" > ~/.streamlit/credentials.toml

echo "\
[server]
headless = true
enableCORS=false
port = $PORT
" > ~/.streamlit/config.toml
