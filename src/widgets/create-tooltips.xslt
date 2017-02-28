<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:exslt="http://exslt.org/common">

<xsl:output method="text" />

<xsl:template match = "/b2">
tooltips = {
   <xsl:for-each select="module">
   '<xsl:value-of select="@name"/>' : {
      <xsl:for-each select="category">
         <xsl:call-template name="switches"/>
      </xsl:for-each>
      }
   </xsl:for-each>
</xsl:template>


   
<xsl:template name="switches">
   <!--xsl:for-each select="concat('/b2/',$string_name,'/paramgroup')"-->
   <xsl:for-each select="switchgroup/switch">
      '<xsl:value-of select="name"/>' : ('<xsl:value-of select="../@name"/>', '<xsl:value-of select="type"/>', """<xsl:value-of select="../description"/>""", '<xsl:value-of select="default"/>'),
   </xsl:for-each>
   <xsl:for-each select="switch">
      '<xsl:value-of select="name"/>' : ('<xsl:value-of select="../@name"/>', '<xsl:value-of select="type"/>', """<xsl:value-of select="description"/>""", '<xsl:value-of select="default"/>'),
   </xsl:for-each>
</xsl:template>
</xsl:stylesheet>