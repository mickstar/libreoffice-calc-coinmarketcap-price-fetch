Function CRYPTOPRICE(CryptocurrencyCode as String, Optional CurrencyCode as String) as Double
	On Error GoTo ErrorHandler
	
	if IsMissing(CurrencyCode) THEN
		CurrencyCode = "USD"
	END IF
  	mspf = GetDefaultContext().getByName("/singletons/com.sun.star.script.provider.theMasterScriptProviderFactory")
 	 sp = mspf.createScriptProvider(ThisComponent.ScriptContainer)
    oScript = sp.getScript("vnd.sun.star.script:CMCPriceGet.py$get_price_from_cmc?language=Python&location=user")
    pycmc = oScript.invoke(array(CryptocurrencyCode, CurrencyCode), array(), array())
	CRYPTOPRICE = pycmc
	Exit Function

ErrorHandler:
    CRYPTOPRICE = -1 ' Return a default error value, you can choose another value if needed
    Resume Next
End Function