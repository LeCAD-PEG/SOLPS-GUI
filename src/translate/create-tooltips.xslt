<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:exslt="http://exslt.org/common">
<!-- See for serializing content of node: http://stackoverflow.com/questions/13362291/xslcopy-of-just-the-content-without-the-node-->
<xsl:output method="html" encoding="UTF-("/>

<xsl:template match="/b2">
# -*- coding: utf-8 -*-

tooltips = {
<xsl:for-each select="module">
<xsl:if test="@name!='b2.parameters'">
'<xsl:value-of select="@name"/>' : {
<xsl:for-each select="category">
<xsl:call-template name="switches"/>
<xsl:call-template name="params"/>
</xsl:for-each>
},
</xsl:if>
<xsl:if test="@name='b2.parameters'">
<xsl:for-each select="category">
'<xsl:value-of select="@name"/>' : {
<xsl:call-template name="switches"/>
<xsl:call-template name="params"/> 
},
</xsl:for-each>
</xsl:if>
</xsl:for-each>
}
</xsl:template>

<xsl:template name="switches">
   <!--xsl:for-each select="concat('/b2/',$string_name,'/paramgroup')"-->
   <xsl:for-each select="switchgroup/switch">
      '<xsl:value-of select="name"/>' : ('<xsl:value-of select="../@name"/>', '<xsl:value-of select="type"/>', """<xsl:copy-of select="../description/node()"/>""", '<xsl:value-of select="default"/>'),
   </xsl:for-each>
   <xsl:for-each select="switch">
      '<xsl:value-of select="name"/>' : ('<xsl:value-of select="../@name"/>', '<xsl:value-of select="type"/>', """<xsl:copy-of select="description/node()"/>""", '<xsl:value-of select="default"/>'),
   </xsl:for-each>
</xsl:template>
   
<xsl:template name="params">
   <!--xsl:for-each select="concat('/b2/',$string_name,'/paramgroup')"-->
   <xsl:for-each select="param">
      '<xsl:value-of select="name"/>' : ('<xsl:value-of select="../@name"/>', '<xsl:value-of select="type"/>', """<xsl:copy-of select="description/node()"/>""", '<xsl:value-of select="default"/>'),
   </xsl:for-each>
</xsl:template>
</xsl:stylesheet>