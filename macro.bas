Function CRYPTOPRICE(CryptocurrencyCode as String, Optional CurrencyCode as String) as Double
	if IsMissing(CurrencyCode) THEN
		CurrencyCode = "USD"
	END IF
    oScriptProvider = ThisComponent.getScriptProvider()
    oScript = oScriptProvider.getScript("vnd.sun.star.script:CMCPriceGet.py$get_price_from_cmc?language=Python&location=user")
    pycmc = oScript.invoke(array(CryptocurrencyCode, CurrencyCode), array(), array())
	CRYPTOPRICE = pycmc
END Function

