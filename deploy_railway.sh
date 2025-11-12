#!/bin/bash
echo "🚀 DEPLOY AUTOMÁTICO A RAILWAY"

# Configurar nuevo token de Railway
export RAILWAY_TOKEN="dd667194-2aad-4fdc-b358-e94742291c22"

echo "🔑 Token Railway configurado"
echo "📦 Subiendo código a GitHub..."

# Configurar Git (necesitamos token GitHub nuevo)
git config --global user.name "Dandro12345"
git config --global user.email "arochapedro2@gmail.com"

# Hacer commit de los cambios
git add .
git commit -m "Deploy a Railway - $(date)"

echo "✅ Código listo para deploy"
echo "📋 Archivos listos:"
ls -la *.py requirements.txt Procfile

echo ""
echo "🎯 PRÓXIMO PASO:"
echo "❌ FALTA: Nuevo token de GitHub"
echo "🌐 Ve a: https://github.com/settings/tokens"
echo "🔨 Genera nuevo token con permisos 'repo'"
echo "📋 Pega el nuevo token aquí"
echo ""
echo "💡 Con ambos tokens, hacemos deploy automático a Railway"
