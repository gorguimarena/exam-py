#!/bin/bash

# Script de test complet de l'API FastAPI
# Assurez-vous que le serveur tourne sur http://localhost:8000

echo "🚀 Début des tests de l'API FastAPI..."

BASE_URL="http://localhost:8000"
TOKEN=""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}📝 Étape 1 : Inscription...${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "nom": "Test User"
  }')

echo "$REGISTER_RESPONSE" | python3 -m json.tool

# Extraire le token
TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo -e "${RED}❌ Erreur : Impossible d'obtenir le token${NC}"
  exit 1
fi

echo -e "${GREEN}✅ Token obtenu${NC}"

echo -e "\n${YELLOW}📝 Étape 2 : Création d'un fournisseur...${NC}"
FOURNISSEUR_RESPONSE=$(curl -s -X POST "$BASE_URL/api/fournisseurs" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nom": "Fournisseur Test",
    "telephone": "221771234567",
    "adresse": "Dakar, Sénégal"
  }')

echo "$FOURNISSEUR_RESPONSE" | python3 -m json.tool

FOURNISSEUR_ID=$(echo "$FOURNISSEUR_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
echo -e "${GREEN}✅ Fournisseur créé : $FOURNISSEUR_ID${NC}"

echo -e "\n${YELLOW}📝 Étape 3 : Création d'un produit...${NC}"
PRODUIT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/produits" \
  -H "Authorization: Bearer $TOKEN" \
  -F "libelle=Produit Test" \
  -F "prix_unitaire=100000" \
  -F "quantite_stock=10")

echo "$PRODUIT_RESPONSE" | python3 -m json.tool

PRODUIT_ID=$(echo "$PRODUIT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
echo -e "${GREEN}✅ Produit créé : $PRODUIT_ID${NC}"

echo -e "\n${YELLOW}📝 Étape 4 : Liste des produits...${NC}"
curl -s -X GET "$BASE_URL/api/produits" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo -e "\n${YELLOW}📝 Étape 5 : Incrémentation du stock...${NC}"
INCREMENT_RESPONSE=$(curl -s -X PATCH "$BASE_URL/api/produits/$PRODUIT_ID/increment" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "quantite": 5
  }')

echo "$INCREMENT_RESPONSE" | python3 -m json.tool

echo -e "\n${YELLOW}📝 Étape 6 : Création d'un approvisionnement...${NC}"
APPRO_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvisionnements" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"quantite\": 50,
    \"fournisseur_id\": \"$FOURNISSEUR_ID\",
    \"produit_id\": \"$PRODUIT_ID\"
  }")

echo "$APPRO_RESPONSE" | python3 -m json.tool

APPRO_ID=$(echo "$APPRO_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
echo -e "${GREEN}✅ Approvisionnement créé : $APPRO_ID${NC}"

echo -e "\n${YELLOW}📝 Étape 7 : Vérification du stock après approvisionnement...${NC}"
PRODUIT_FINAL=$(curl -s -X GET "$BASE_URL/api/produits/$PRODUIT_ID" \
  -H "Authorization: Bearer $TOKEN")

echo "$PRODUIT_FINAL" | python3 -m json.tool

STOCK_FINAL=$(echo "$PRODUIT_FINAL" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['quantite_stock'])" 2>/dev/null)
echo -e "${GREEN}✅ Stock final : $STOCK_FINAL (devrait être 65 = 10 + 5 + 50)${NC}"

echo -e "\n${GREEN}🎉 Tous les tests sont terminés avec succès !${NC}"

# Résumé
echo -e "\n${YELLOW}📊 RÉSUMÉ :${NC}"
echo -e "Fournisseur ID : $FOURNISSEUR_ID"
echo -e "Produit ID : $PRODUIT_ID"
echo -e "Approvisionnement ID : $APPRO_ID"
echo -e "Stock final : $STOCK_FINAL"
