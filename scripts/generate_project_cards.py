#!/usr/bin/env python3
"""Regenerate the typographic project cards. Requires Pillow, not used by the site build."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--serif',default='/System/Library/Fonts/Supplemental/Georgia.ttf')
    parser.add_argument('--sans',default='/System/Library/Fonts/Supplemental/Arial.ttf')
    parser.add_argument('--only',default=None,help='Generate only the card matching this slug')
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    cards=[
        ('projects','Projects','AI workflows, photography and independent software.','Projects by Diogo Silva'),
        ('bronze-clinical','Bronze Clinical','Websites for private medical and dental clinics.','Photography · Video · Writing · Web development'),
        ('bronze-art-galleries','Bronze Art','Documentary photography of family life and faith.','Photography portfolio · Private client galleries'),
        ('cutline','Cutline','Local video clipping for Mac.','Transcription · Vertical framing · Editable captions'),
        ('vitachart','VitaChart','A fertility diary built from family experience.','Creighton and Billings · Reports for consultations'),
    ]
    if args.only:
        cards=[c for c in cards if c[0]==args.only]
        if not cards:
            raise SystemExit(f'Unknown card slug: {args.only}')
    for slug,title,subtitle,detail in cards:
        img=Image.new('RGB',(1200,630),'#FBFAF7')
        draw=ImageDraw.Draw(img)
        sans=ImageFont.truetype(args.sans,26)
        small=ImageFont.truetype(args.sans,22)
        serif=ImageFont.truetype(args.serif,90 if '\n' in title else 104)
        sub=ImageFont.truetype(args.serif,30)
        draw.text((80,52),'DIOGO SILVA',font=sans,fill='#56534C')
        draw.line((80,112,1120,112),fill='#CEC8BD',width=1)
        draw.multiline_text((76,166),title,font=serif,fill='#191814',spacing=4)
        draw.line((80,391,144,391),fill='#8A6A3C',width=3)
        assert draw.textbbox((0,0),subtitle,font=sub)[2]<=1040
        draw.text((80,418),subtitle,font=sub,fill='#56534C')
        draw.text((80,482),detail,font=small,fill='#746E63')
        draw.text((80,560),'DIOGOBRONZESILVA.COM',font=small,fill='#746E63')
        img.save(args.output/(slug+'.jpg'),quality=92,optimize=True)
    print(f'Generated {len(cards)} 1200 × 630 project card(s).')

if __name__=='__main__':main()
